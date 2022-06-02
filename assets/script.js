var header;
var btnHide;
var btnShow;
var sidebar;
var map;
var sidebarHandle;
var movingSidebar = false;

document.addEventListener('mouseover', function(e) {
    if (typeof(header) === 'undefined' || typeof(btnHide) === 'undefined' || typeof(btnShow) === 'undefined') {
        sidebar = document.getElementsByClassName('sidebar')[0];
        sidebarHandle = document.getElementsByClassName('sidebar-handle')[0];
        header = document.getElementsByClassName('header')[0];
        btnHide = document.getElementsByClassName('hide-header')[0];
        btnShow = document.getElementsByClassName('show-header')[0];
        map = document.getElementsByClassName('map-box')[0];
        btnHide.addEventListener('mousedown', hideHeader);
        btnShow.addEventListener('mousedown', showHeader);
        sidebarHandle.addEventListener('mousedown', moveSidebar);
        sidebarHandle.addEventListener('mouseup', stopMoveSidebar);
    }
});

document.addEventListener('mousemove', function(e) {
    if (typeof(sidebar) != 'undefined' || typeof(sidebarHandle) != 'undefined') {
        if (movingSidebar == true) {
            var posX = window.event.clientX;
            sidebar.style.width = `${posX}px`;
            sidebar.style.minWidth = `${posX}px`;
            sidebarHandle.style.left = `${posX}px`;
        }
    }
});

document.addEventListener('scroll', function(e) {
    sidebar.style.marginTop = `${document.documentElement.scrollTop + 2}px`;
    var pos = map.getBoundingClientRect().top;
    if (pos <= 40 && pos > 0 && header.style.display != 'none') {
        hideHeader()
        document.documentElement.scrollTop = 0;
    } else if (pos <= 40) {
        btnShow.style.visibility = 'visible';
    }
});

function showHeader() {
    document.documentElement.scrollTop = 0;
    header.style.display = 'block';
    btnShow.style.visibility = 'hidden';
}
function hideHeader() {
    header.style.display = 'none';
    btnShow.style.visibility = 'visible';
}
function moveSidebar() {
    movingSidebar = true;
}
function stopMoveSidebar() {
    movingSidebar = false;
}
















// class DomUtils {
    // static keys = { 37: 1, 38: 1, 39: 1, 40: 1 };
// 
    // static preventDefault(e) {
      // e = e || window.event;
      // if (e.preventDefault) e.preventDefault();
      // e.returnValue = false;
    // }
// 
    // static preventDefaultForScrollKeys(e) {
      // if (DomUtils.keys[e.keyCode]) {
        // DomUtils.preventDefault(e);
        // return false;
      // }
    // }
// 
    // static disableScroll() {
      // document.addEventListener('wheel', DomUtils.preventDefault, {
        // passive: false,
      // }); // Disable scrolling in Chrome
      // document.addEventListener('keydown', DomUtils.preventDefaultForScrollKeys, {
        // passive: false,
      // });
    // }
// 
    // static enableScroll() {
      // document.removeEventListener('wheel', DomUtils.preventDefault, {
        // passive: false,
      // }); // Enable scrolling in Chrome
      // document.removeEventListener(
        // 'keydown',
        // DomUtils.preventDefaultForScrollKeys,
        // {
          // passive: false,
        // }
      // ); // Enable scrolling in Chrome
    // }
  // }
// 
// DomUtils.disableScroll()
