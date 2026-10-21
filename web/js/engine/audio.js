/* ==========================================================================
   engine/audio.js
   三条通道：music / sound / voice（+ menu_music）。
   对应 Ren'Py 的 play / stop / queue 与 fadein / fadeout / volume / loop。
   ========================================================================== */
(function (global) {
  'use strict';

  /*
   * 重要：本文件在 IIFE 内声明了 function Audio(...)（音频管理器）。
   * 函数声明会提升到整个 IIFE 作用域，因此在本文件内写 `new Audio()`
   * 实际会递归调用这个管理器，造成栈溢出。
   * 统一改用 document.createElement('audio') 创建原生元素。
   */
  function createAudioElement() {
    var el = document.createElement('audio');
    el.preload = 'auto';
    el.loop = false;
    return el;
  }

  function Channel(name, owner) {
    this.name = name;
    this.owner = owner;
    this.el = createAudioElement();
    this.el.preload = 'auto';
    this.el.loop = false;
    this.current = null;      /* 当前路径 */
    this.fadeTimer = null;
    this.volume = 1.0;
  }

  Channel.prototype.setVolume = function (v, seconds) {
    v = Math.max(0, Math.min(1, v));
    var from = this.el.volume;
    this.volume = v;
    this.clearFade();
    if (!seconds) { this.el.volume = v; return; }
    var start = performance.now();
    var ms = seconds * 1000;
    var el = this.el;
    var self = this;
    this.fadeTimer = setInterval(function () {
      var t = (performance.now() - start) / ms;
      if (t >= 1) {
        el.volume = v;
        self.clearFade();
        return;
      }
      el.volume = from + (v - from) * t;
    }, 40);
  };

  Channel.prototype.clearFade = function () {
    if (this.fadeTimer) { clearInterval(this.fadeTimer); this.fadeTimer = null; }
  };

  Channel.prototype.play = function (url, opts) {
    opts = opts || {};
    var self = this;
    this.clearFade();

    var sameSrcLoaded = this.current === url &&
      this.el.getAttribute('src') &&
      this.el.readyState > 0;

    if (sameSrcLoaded) {
      /* 同一资源已在位：只调整循环/音量，不动 src —— 避免请求被打断产生
         NS_BINDING_ABORTED */
      this.el.loop = !!opts.loop;
      var v0 = opts.volume == null ? this.owner.volumeFor(this.name) : opts.volume;
      this.el.volume = v0;
      this.volume = v0;
      if (this.el.paused) this.tryPlay();
      return this;
    }

    this.el.pause();
    /* preload 设为 auto 再赋值，减少 play() 时二次加载导致的中断 */
    this.el.preload = 'auto';
    this.el.src = url;
    this.el.loop = !!opts.loop;
    this.current = url;

    var targetVol = opts.volume == null ? this.owner.volumeFor(this.name) : opts.volume;
    this.el.volume = opts.fadein ? 0 : targetVol;
    this.volume = targetVol;

    this.tryPlay();

    if (opts.fadein) this.setVolume(targetVol, opts.fadein);
    return this;
  };

  /**
   * 尝试播放。自动播放被拦截时登记为「等首次交互」，不重试、不抛噪音。
   */
  Channel.prototype.tryPlay = function () {
    var self = this;
    var p = this.el.play();
    if (p && p.catch) {
      p.catch(function (err) {
        /* AbortError：src 被替换，属正常竞态，忽略 */
        if (err && err.name === 'AbortError') return;
        /* NotAllowedError：自动播放策略，等首次交互 */
        self.owner.pendingAutoplay = function () {
          var p2 = self.el.play();
          if (p2 && p2.catch) p2.catch(function () {});
        };
      });
    }
  };

  Channel.prototype.stop = function (opts) {
    opts = opts || {};
    var self = this;
    if (!opts.fadeout) {
      this.el.pause();
      this.el.currentTime = 0;
      this.current = null;
      return;
    }
    var from = this.el.volume;
    var ms = opts.fadeout * 1000;
    var start = performance.now();
    this.clearFade();
    this.fadeTimer = setInterval(function () {
      var t = (performance.now() - start) / ms;
      if (t >= 1) {
        self.el.volume = from;
        self.el.pause();
        self.el.currentTime = 0;
        self.current = null;
        self.clearFade();
        return;
      }
      self.el.volume = from * (1 - t);
    }, 40);
  };

  Channel.prototype.isPlaying = function () {
    return !!this.current && !this.el.paused;
  };

  /* --------------------------------------------------------------------------
     Audio 管理器
     -------------------------------------------------------------------------- */
  function Audio(images, state, persistent) {
    this.images = images;
    this.state = state;
    this.persistent = persistent;
    this.pendingAutoplay = null;

    this.music = new Channel('music', this);
    this.sound = new Channel('sound', this);
    this.voice = new Channel('voice', this);
    this.menuMusic = new Channel('menu_music', this);

    this.currentVoiceTag = null;

    var self = this;
    /* 首次交互后补播被拦截的音频 */
    var unlock = function () {
      if (self.pendingAutoplay) {
        var fn = self.pendingAutoplay;
        self.pendingAutoplay = null;
        fn();
      }
      global.removeEventListener('pointerdown', unlock);
      global.removeEventListener('keydown', unlock);
    };
    global.addEventListener('pointerdown', unlock, { passive: true });
    global.addEventListener('keydown', unlock);
  }

  Audio.prototype.channelOf = function (name) {
    switch (name) {
      case 'music':
      case 'menu_music': return name === 'menu_music' ? this.menuMusic : this.music;
      case 'sound':
      case 'audio':
      case 'ambient': return this.sound;
      case 'voice': return this.voice;
      case 'movie': return null;   /* 由 movie.js 处理 */
      default: return null;
    }
  };

  Audio.prototype.volumeFor = function (channel) {
    var p = this.persistent.data;
    if (channel === 'music') return num(p.music_volume, 0.9);
    if (channel === 'sound') return num(p.sound_volume, 0.9);
    if (channel === 'voice') {
      var base = num(p.voice_volume, 0.9);
      var per = this.currentVoiceTag && p.character_volume
        ? num(p.character_volume[this.currentVoiceTag], 1.0)
        : 1.0;
      return base * per;
    }
    if (channel === 'menu_music') return num(p.music_volume, 0.9);
    return 1.0;
  };

  function num(v, d) {
    var n = parseFloat(v);
    return isNaN(n) ? d : n;
  }

  Audio.prototype.play = function (channel, path, opts) {
    var ch = this.channelOf(channel);
    if (!ch || !path) return;

    /* 统一走 images.url()：它会补 ../ 根前缀、处理中文编码与回退表 */
    var url = this.images.url(path, 'audio');
    if (!url) return;

    ch.play(url, opts || {});

    if (channel === 'music') {
      this.state.music = { path: path, loop: !!(opts && opts.loop) };
    }
    if (channel === 'sound' || channel === 'ambient') {
      this.state.ambient = { path: path, loop: !!(opts && opts.loop) };
    }
  };

  Audio.prototype.stop = function (channel, opts) {
    var ch = this.channelOf(channel);
    if (!ch) return;
    ch.stop(opts || {});
    if (channel === 'music') this.state.music = null;
    if (channel === 'sound' || channel === 'ambient') this.state.ambient = null;
  };

  Audio.prototype.playVoice = function (path, voiceTag) {
    if (!path) return;
    this.currentVoiceTag = voiceTag || guessTag(path);

    var url = this.images.url(path, 'audio');
    if (!url) return;

    this.voice.play(url, { loop: false });
    this.state.voice = { path: path };
  };

  function guessTag(path) {
    var p = String(path);
    if (p.indexOf('linxi') >= 0) return 'lx';
    if (p.indexOf('jiangwanqing') >= 0) return 'jwq';
    if (p.indexOf('xiaolian') >= 0) return 'xl';
    return null;
  }

  Audio.prototype.stopVoice = function () {
    this.voice.stop({});
    this.state.voice = null;
  };

  /** 语音是否还在播（auto 模式等待用） */
  Audio.prototype.isVoicePlaying = function () {
    return this.voice.isPlaying();
  };

  Audio.prototype.onVoiceEnded = function (cb) {
    this.voice.el.onended = cb;
  };

  Audio.prototype.applyVolumes = function () {
    var self = this;
    ['music', 'sound', 'voice', 'menu_music'].forEach(function (k) {
      var ch = self[k === 'menu_music' ? 'menuMusic' : k];
      ch.el.volume = self.volumeFor(k);
      ch.volume = ch.el.volume;
    });
  };

  Audio.prototype.pauseAll = function () {
    this.music.el.pause();
    this.sound.el.pause();
    this.voice.el.pause();
  };

  Audio.prototype.resumeAll = function () {
    if (this.state.music && this.music.current) this.music.tryPlay();
    if (this.state.ambient && this.sound.current) this.sound.tryPlay();
  };

  global.RPYAudio = {
    Audio: Audio,
    Channel: Channel,
    createAudioElement: createAudioElement
  };
})(window);