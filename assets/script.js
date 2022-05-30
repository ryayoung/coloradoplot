class DomUtils {
    // left: 37, up: 38, right: 39, down: 40,
    // spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
    static keys = { 37: 1, 38: 1, 39: 1, 40: 1 };
  
    static preventDefault(e) {
      e = e || window.event;
      if (e.preventDefault) e.preventDefault();
      e.returnValue = false;
    }
  
    static preventDefaultForScrollKeys(e) {
      if (DomUtils.keys[e.keyCode]) {
        DomUtils.preventDefault(e);
        return false;
      }
    }
  
    static disableScroll() {
      document.addEventListener('wheel', DomUtils.preventDefault, {
        passive: false,
      }); // Disable scrolling in Chrome
      document.addEventListener('keydown', DomUtils.preventDefaultForScrollKeys, {
        passive: false,
      });
    }
  
    static enableScroll() {
      document.removeEventListener('wheel', DomUtils.preventDefault, {
        passive: false,
      }); // Enable scrolling in Chrome
      document.removeEventListener(
        'keydown',
        DomUtils.preventDefaultForScrollKeys,
        {
          passive: false,
        }
      ); // Enable scrolling in Chrome
    }
  }

// DomUtils.disableScroll()

var header;
var btnHide;
var btnShow;

document.addEventListener('mouseover', function(e) {
    if (typeof(header) === 'undefined' || typeof(btnHide) === 'undefined' || typeof(btnShow) === 'undefined') {
        header = document.getElementsByClassName('header')[0];
        btnHide = document.getElementsByClassName('hide-header-btn')[0];
        btnShow = document.getElementsByClassName('show-header-btn')[0];
        btnHide.addEventListener('click', hideHeader);
        btnShow.addEventListener('click', showHeader);
    }
});

document.addEventListener('mouseover', function(e) {
    if (typeof(header) === 'undefined' || typeof(btnHide) === 'undefined' || typeof(btnShow) === 'undefined') {
        header = document.getElementsByClassName('header')[0];
        btnHide = document.getElementsByClassName('hide-header-btn')[0];
        btnShow = document.getElementsByClassName('show-header-btn')[0];
        btnHide.addEventListener('click', hideHeader);
        btnShow.addEventListener('click', showHeader);
    }
});

document.addEventListener('scroll', function(e) {
    var map = document.getElementsByClassName('map-box')[0];
    var pos = map.getBoundingClientRect().top;
    if (pos <= 10) {
        hideHeader()
        btnShow.style.visibility = 'visible'
    }
});

function showHeader() {
    header.style.display = 'block';
    btnShow.style.visibility = 'hidden';
    document.documentElement.scrollTop = 0;
}
function hideHeader() {
    header.style.display = 'none';
    btnShow.style.visibility = 'visible';
    document.documentElement.scrollTop = 0;
}







// var btn;


// function backToTop() {
//     document.documentElement.scrollTop = 0;
// }