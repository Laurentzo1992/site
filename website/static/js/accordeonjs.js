/*
 * Copyright © 2006 2024. Kortic (URL : https://www.kortic.com/accordeons-html-accessibles-avec-balises-details-et-summary.html)
 * licence Creative Commons CC BY-NC-SA 4.0
 * https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
 */
 
;((__) => {
    'use strict';
    /*
    Cette fonction utilise
      const KEYCODES = {
        BACKSPACE: 8,
        TAB: 9,
        SHIFT_TAB: 16,
        ENTER: 13,
        ESC: 27,
        SPACE: 32,
        PAGEUP:33,
        PAGEDOWN:34,
        END: 35,
        HOME: 36,
        LEFT: 37,
        UP: 38,
        RIGHT: 39,
        DOWN: 40
      };
      const DOM = {
        document:  jQuery(document),
        body:  jQuery('body').first(),
        main:    jQuery('body > main').first()
      };
    et
      jQuery.fn.doOnce = function (func) {
        this.length && func.apply(this);
        return this;
      };
     */
    __.details = (node) => {
      let from = node === undefined ? DOM.body : node;
      // keyboard loop Up/Down Arrow
      let loop = true,
      // désactive les animations slideUp/slideDown si terminal configuré
      duration = !window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 200 : 0;
      let details = from.find('details');
      details.each(function () {
        let details_ = __(this),
          summary = details_.find('summary').first(),
          txt = ' ' + summary.text();
        summary.attr({
          'aria-label': __.means(
            details_.attr('open') === undefined
              ? 'accordion_open_label'
              : 'accordion_close_label'
          ) + txt
        });
        summary.on({
          click: e => {
            e.preventDefault();
            if (details_.attr('open') === undefined) {
              details_.attr({
                'open': true
              });
              summary.next().hide().slideDown(duration, 'linear', () => {
                summary.attr({
                  'aria-label': __.means('accordion_close_label') + txt
                });
              });
            } else {
              summary.next().slideUp(duration, 'linear', () => {
                details_.attr({
                  'open': null
                });
                summary.attr({
                  'aria-label': __.means('accordion_open_label') + txt
                });
              });
            }
            /*
             Vérification de la présence d'un attribut data-details-toggle
             pour ouvrir/fermer les details se trouvant dans le même conteneur
            */
            if (details_.attr('data-details-toggle') !== undefined) {
              let getOther = __('#' + details_.attr('data-details-toggle')).find('details[open]').not(details_);
              getOther.length && getOther.find('summary').next().slideUp(duration, 'linear', () => {
                getOther.attr('open', null);
                let currentSummary = getOther.find('summary'),
                  ariaLabel = currentSummary.attr('aria-label');
                currentSummary.attr('aria-label', ariaLabel.replace(__.means('accordion_close_label'), __.means('accordion_open_label')));
              });
            }
          },
          keydown: e => {
            let target_ = __(e.target);
            __.inArray(e.keyCode, [KEYCODES.SPACE, KEYCODES.ENTER, KEYCODES.UP, KEYCODES.DOWN]) !== -1 && e.preventDefault();
            __.inArray(e.keyCode, [KEYCODES.SPACE, KEYCODES.ENTER]) !== -1 && target_.trigger('click');
            if (details_.attr('data-details-toggle') === undefined) {
              let parent_ = target_.parent();
              e.keyCode === KEYCODES.UP && parent_.prev('details').find('summary').trigger('focus');
              e.keyCode === KEYCODES.DOWN && parent_.next('details').find('summary').trigger('focus');
              if (loop) {
                (e.keyCode === KEYCODES.DOWN) && (!parent_.next('details').length && parent_.parent().find('summary').first().trigger('focus'));
                (e.keyCode === KEYCODES.UP) && (!parent_.prev('details').length && parent_.parent().find('summary').last().trigger('focus'));
              }
            } else {
              let parent_ = __('#' + details_.attr('data-details-toggle')),
                list = parent_.find('details');
              if(parent_.attr('data-init') === undefined) {
                list.each(function (i) {
                  __(list[i]).attr({
                    'data-index': i,
                    'data-prev': i === 0 ? list.length-1 : i-1,
                    'data-next': i === list.length-1 ? 0 : i+1
                  });
                });
                parent_.attr('data-init', '1');
              }
              let current = __(this);
              if(loop) {
                e.keyCode === KEYCODES.UP && parent_.find('[data-index="'+ current.attr('data-prev') +'"]').find('summary').trigger('focus');
                e.keyCode === KEYCODES.DOWN && parent_.find('[data-index="'+ current.attr('data-next') +'"]').find('summary').trigger('focus');
              } else {
                (e.keyCode === KEYCODES.UP && current.data('index') !== 0) && parent_.find('[data-index="'+ current.attr('data-prev') +'"]').find('summary').trigger('focus');
                (e.keyCode === KEYCODES.DOWN && current.data('index') !== list.length-1) && parent_.find('[data-index="'+ current.attr('data-next') +'"]').find('summary').trigger('focus');
              }
            }
          }
        })
      });
    };
    DOM.document.ready(__.details());
  })(jQuery);