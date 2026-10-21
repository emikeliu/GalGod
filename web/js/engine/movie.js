/* ==========================================================================
   engine/movie.js
   ED 视频播放。对应 script.rpy 的 ed_player 屏幕（全屏、锁输入）。
   ========================================================================== */
(function (global) {
  'use strict';

  function Movie(app) {
    this.app = app;
    this.layer = document.getElementById('layer-movie');
    this.video = null;
    this.resolve = null;
  }

  Movie.prototype.show = function (path) {
    var self = this;
    this.hide();

    var url = String(path).split('/').map(function (s) {
      return encodeURIComponent(s);
    }).join('/');

    var v = document.createElement('video');
    v.src = url;
    v.style.cssText =
      'position:absolute;inset:0;width:100%;height:100%;' +
      'object-fit:contain;background:#000;';
    v.playsInline = true;
    v.preload = 'auto';
    v.controls = false;

    this.layer.innerHTML = '';
    this.layer.appendChild(v);
    this.layer.hidden = false;
    this.video = v;

    /* 全屏锁定输入 */
    this.lockInput(true);

    v.addEventListener('ended', function () {
      self.app.vm.resume();
    });

    var p = v.play();
    if (p && p.catch) p.catch(function () {
      /* 自动播放被拦截：给一个可点击的播放覆盖层 */
      var btn = document.createElement('button');
      btn.textContent = '▶ 播放片尾';
      btn.style.cssText =
        'position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);' +
        'padding:20px 48px;font-size:24px;border-radius:8px;' +
        'border:1px solid rgba(255,255,255,.4);background:rgba(0,0,0,.6);' +
        'color:#fff;cursor:pointer;font-family:inherit;';
      btn.addEventListener('click', function () {
        btn.remove();
        v.play();
      });
      self.layer.appendChild(btn);
    });

    return new Promise(function (resolve) {
      self.resolve = resolve;
      v.addEventListener('ended', function () { resolve(); });
    });
  };

  Movie.prototype.hide = function () {
    this.lockInput(false);
    if (this.video) {
      this.video.pause();
      this.video.removeAttribute('src');
      this.video.load();
      this.video = null;
    }
    this.layer.innerHTML = '';
    this.layer.hidden = true;
    if (this.resolve) {
      var r = this.resolve;
      this.resolve = null;
      r();
    }
  };

  Movie.prototype.lockInput = function (on) {
    this.locked = !!on;
    var screens = document.getElementById('layer-screens');
    screens.style.pointerEvents = on ? 'none' : 'auto';
  };

  Movie.prototype.isPlaying = function () {
    return !!this.video;
  };

  global.RPYMovie = {
    Movie: Movie
  };
})(window);