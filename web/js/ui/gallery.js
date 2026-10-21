/* ==========================================================================
   ui/gallery.js
   附加鉴赏。对应 screens/gallery.rpy：
   3×3 网格、每页 9 项、可翻页、点击全屏查看、通关后解锁。
   ========================================================================== */
(function (global) {
  'use strict';

  /* 与 screens/gallery.rpy 的 gallery_buttons 对应的条目 */
  var ITEMS = [
    { id: 'cg001', label: '月幕',        img: 'images/cg/001.avif', unlock: 'ACH_01' },
    { id: 'cg002', label: '归家',        img: 'images/cg/002.avif', unlock: 'ACH_02' },
    { id: 'cg003', label: '雨夜',        img: 'images/cg/003.avif', unlock: 'ACH_03' },
    { id: 'cg004', label: '记忆',        img: 'images/cg/004.avif', unlock: 'ACH_04' },
    { id: 'cg005', label: '告白',        img: 'images/cg/005.avif', unlock: 'ACH_05' },
    { id: 'cg006', label: '同行',        img: 'images/cg/006.avif', unlock: 'ACH_06' },
    { id: 'cg007', label: '展翅',        img: 'images/cg/007.avif', unlock: 'ACH_07' },
    { id: 'cg008', label: '尾声',        img: 'images/cg/008.avif', unlock: 'ACH_08' },
    { id: 'cg009', label: '月下',        img: 'images/cg/009.avif', unlock: null },
    { id: 'sdcg01', label: 'SD · 01',    img: 'images/sdcg/001.avif', unlock: null },
    { id: 'sdcg02', label: 'SD · 02',    img: 'images/sdcg/002.avif', unlock: null },
    { id: 'sdcg03', label: 'SD · 03',    img: 'images/sdcg/003.avif', unlock: null },
    { id: 'sdcg04', label: 'SD · 04',    img: 'images/sdcg/004.avif', unlock: null },
    { id: 'sdcg05', label: 'SD · 05',    img: 'images/sdcg/005.avif', unlock: null },
    { id: 'sdcg07', label: 'SD · 07',    img: 'images/sdcg/007.avif', unlock: null },
    { id: 'sdcg08', label: 'SD · 08',    img: 'images/sdcg/008.avif', unlock: null },
    { id: 'sdcg10', label: 'SD · 10',    img: 'images/sdcg/010.avif', unlock: null },
    { id: 'noctella', label: '诺提拉降临', img: 'images/cg/noctella_descend.webp', unlock: 'ACH_08' }
  ];

  var PER_PAGE = 9;

  function GalleryUI(app) {
    this.app = app;
    this.el = null;
    this.page = 0;
  }

  GalleryUI.prototype.isOpen = function () {
    return !!this.el;
  };

  GalleryUI.prototype.open = function () {
    if (this.el) return;
    var self = this;

    var root = document.createElement('div');
    root.className = 'menu-screen dim';
    root.id = 'menu-gallery';

    var body = document.createElement('div');
    body.className = 'gl-body';

    var head = document.createElement('div');
    head.className = 'sl-head';
    var title = document.createElement('div');
    title.className = 'menu-title';
    title.textContent = '附加鉴赏';
    var close = document.createElement('button');
    close.type = 'button';
    close.textContent = '返回';
    close.style.cssText =
      'height:46px;padding:0 26px;border:1px solid rgba(255,255,255,.3);' +
      'border-radius:4px;background:rgba(255,255,255,.08);color:#ddd;' +
      'font-family:inherit;font-size:17px;cursor:pointer;';
    close.addEventListener('click', function () { self.close(); });
    head.appendChild(title);
    head.appendChild(close);

    var grid = document.createElement('div');
    grid.className = 'gl-grid';

    var foot = document.createElement('div');
    foot.className = 'gl-foot';

    body.appendChild(head);
    body.appendChild(grid);
    body.appendChild(foot);
    root.appendChild(body);

    this.root = root;
    this.grid = grid;
    this.foot = foot;
    this.el = root;

    this._esc = function (e) {
      if (e.key === 'Escape') { e.preventDefault(); self.close(); }
    };
    document.addEventListener('keydown', this._esc);

    this.app.stage.menusLayer.appendChild(root);
    this.render();
  };

  GalleryUI.prototype.close = function () {
    if (!this.el) return;
    this.el.parentNode.removeChild(this.el);
    this.el = null;
    if (this._esc) {
      document.removeEventListener('keydown', this._esc);
      this._esc = null;
    }
  };

  GalleryUI.prototype.isUnlocked = function (item) {
    /* 未指定解锁条件的条目默认可用；其余需对应成就 */
    if (!item.unlock) return true;
    return !!this.app.state.achievements[item.unlock] ||
           !!this.app.state.persistent.get('achievements.' + item.unlock) ||
           !!this.app.state.persistent.get('game_cleared');
  };

  GalleryUI.prototype.render = function () {
    var self = this;
    var maxPage = Math.max(0, Math.ceil(ITEMS.length / PER_PAGE) - 1);
    if (this.page > maxPage) this.page = maxPage;

    var slice = ITEMS.slice(this.page * PER_PAGE, this.page * PER_PAGE + PER_PAGE);
    this.grid.innerHTML = '';

    slice.forEach(function (item) {
      var unlocked = self.isUnlocked(item);
      var cell = document.createElement('button');
      cell.type = 'button';
      cell.className = 'gl-cell' + (unlocked ? '' : ' locked');
      cell.disabled = !unlocked;

      if (unlocked) {
        var url = self.app.images.url(item.img, 'image');
        var im = document.createElement('img');
        im.src = url || '';
        im.alt = item.label;
        im.loading = 'lazy';
        cell.appendChild(im);
        cell.addEventListener('click', function () { self.view(item); });
      } else {
        cell.style.background = '#111';
      }
      self.grid.appendChild(cell);
    });

    /* 补足空格 */
    for (var i = slice.length; i < PER_PAGE; i++) {
      var empty = document.createElement('div');
      empty.className = 'gl-cell locked';
      empty.style.background = '#0a0a0a';
      this.grid.appendChild(empty);
    }

    /* 翻页 */
    this.foot.innerHTML = '';
    var prev = document.createElement('button');
    prev.type = 'button';
    prev.textContent = '上一页';
    prev.disabled = this.page === 0;
    prev.addEventListener('click', function () {
      if (self.page > 0) { self.page--; self.render(); }
    });

    var info = document.createElement('span');
    info.style.cssText = 'color:rgba(255,255,255,.6);font-size:17px;';
    info.textContent = (this.page + 1) + ' / ' + (maxPage + 1);

    var next = document.createElement('button');
    next.type = 'button';
    next.textContent = '下一页';
    next.disabled = this.page >= maxPage;
    next.addEventListener('click', function () {
      if (self.page < maxPage) { self.page++; self.render(); }
    });

    this.foot.appendChild(prev);
    this.foot.appendChild(info);
    this.foot.appendChild(next);
  };

  GalleryUI.prototype.view = function (item) {
    var self = this;
    var viewer = document.createElement('div');
    viewer.className = 'gl-viewer';

    var url = this.app.images.url(item.img, 'image');
    var im = document.createElement('img');
    im.src = url || '';
    im.alt = item.label;

    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'gl-close';
    close.textContent = '关闭';
    close.addEventListener('click', function () {
      viewer.parentNode.removeChild(viewer);
    });

    viewer.appendChild(im);
    viewer.appendChild(close);
    viewer.addEventListener('click', function (e) {
      if (e.target === viewer) viewer.parentNode.removeChild(viewer);
    });

    this.root.appendChild(viewer);
  };

  global.RPYGalleryUI = {
    GalleryUI: GalleryUI,
    ITEMS: ITEMS
  };
})(window);