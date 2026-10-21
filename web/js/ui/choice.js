/* ==========================================================================
   ui/choice.js
   选项菜单。对应 screens/choice_screen.rpy。
   题面（"???" "题目"）在菜单上方显示。
   ========================================================================== */
(function (global) {
  'use strict';

  var S = global.RPYStrings;

  function ChoiceUI(app) {
    this.app = app;
    this.layer = document.getElementById('choice-layer');
    this.resolve = null;
    this.active = false;
  }

  /**
   * @param {string} caption 题面
   * @param {string} who     题面说话者
   * @param {Array<{text,index,target}>} options
   * @returns {Promise<number>} 选中的 index
   */
  ChoiceUI.prototype.show = function (caption, who, options) {
    var self = this;
    this.active = true;

    /* 有题面时：先当作一句对白播完，再出选项 */
    var render = function () {
      self.layer.innerHTML = '';
      self.layer.hidden = false;

      var list = document.createElement('div');
      list.className = 'choice-list';

      if (caption) {
        var cap = document.createElement('div');
        cap.className = 'choice-caption';
        cap.style.cssText =
          'width:1200px;margin-bottom:26px;font-size:31px;line-height:1.7;' +
          'color:#fff;text-align:center;white-space:pre-wrap;' +
          'text-shadow:2px 0 0 #000,-2px 0 0 #000,0 2px 0 #000,0 -2px 0 #000;';
        cap.innerHTML = S.renderText(caption, 31);
        list.appendChild(cap);
      }

      options.forEach(function (opt) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'choice-button';
        btn.innerHTML = S.renderText(opt.text, 33);
        btn.addEventListener('click', function (e) {
          e.stopPropagation();
          self.pick(opt.index);
        });
        list.appendChild(btn);
      });

      self.layer.appendChild(list);
    };

    return new Promise(function (resolve) {
      self.resolve = resolve;

      if (caption) {
        /* 题面走 say 通道，玩家点击后再显示选项 */
        self.app.ui.say.show(
          { who: who, text: caption, args: { positional: [], kwargs: {} } },
          self.app.vm
        ).then(function () {
          /* say 结束后由点击推进触发，这里等其 resolve 后再渲染 */
          render();
        });
      } else {
        render();
      }
    });
  };

  ChoiceUI.prototype.pick = function (index) {
    if (!this.active) return;
    this.active = false;
    this.layer.hidden = true;
    this.layer.innerHTML = '';
    var r = this.resolve;
    this.resolve = null;
    if (r) r(index);
  };

  ChoiceUI.prototype.hide = function () {
    this.active = false;
    this.layer.hidden = true;
    this.layer.innerHTML = '';
    if (this.resolve) {
      var r = this.resolve;
      this.resolve = null;
      r(-1);
    }
  };

  ChoiceUI.prototype.isActive = function () {
    return this.active;
  };

  global.RPYChoiceUI = {
    ChoiceUI: ChoiceUI
  };
})(window);