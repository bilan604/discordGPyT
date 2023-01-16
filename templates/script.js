function refreshTest(e) {
    var java = require('java');
    var javaLangSystem = java.import('java.lang.System');

    var game = java.import('games.ConnectFour');
    
    alert(newInnerHTML);
    game.makeValidMove(true, "X");
    resultTest.innerHTML = newInnerHTML;
    
    var resultTest = document.getElementById("result_test");
    
  }


  function onMouseUp(e) {
    var gallery = document.getElementById("gallery");
    gallery.mousedown = 'false';
    posdiff = 100 * (e.clientX - gallery.startClick) / window.innerWidth;
    
    gallery.oldpos = posdiff + gallery.oldpos;
    gallery.animate(
        {transform: 'translate(-' + Math.min(100, Math.max(0, gallery.oldpos)) +'%, -44%)'}, 
        {duration: 800, fill: 'forwards'}
      );
  }
  
  function onMouseDown(e) {
    var gallery = document.getElementById("gallery");
    if (isNaN(gallery.oldpos)) {
      gallery.oldpos = 0;
    }
    gallery.startClick = e.clientX;
    gallery.mousedown = 'true';
  }
    
  function onMouseMove(e) {
    const gallery = document.getElementById("gallery");
    const dwindowratio = (e.clientX - gallery.startClick) / window.innerWidth;
    const newratio = 130 * dwindowratio;
    const newpos = newratio + gallery.oldpos;
    if (gallery.mousedown == "true") {
      gallery.animate(
        {transform: 'translate(-' + Math.min(100, Math.max(0, newpos)) +'%, -50%)'}, 
        {duration: 1200, fill: 'forwards'}
      );

      const np = Math.min(100, Math.max(0, (100-(1.5*newpos.toFixed(0)))));
      const images = gallery.getElementsByClassName("image");
      for (let i = 0; i < images.length; i++) {
        images[i].animate(
          {objectPosition: np + '% 50%'},
          {duration: 1200, fill: 'forwards'}
        );
      }
    }
  }
  
  function onMouseEnter(e) {
    /*var element = document.getElementById("test-display");
    element.innerHTML = "<div>Mouse Inside | Inside another div</div>";*/
  }
  
  function onMouseOut(e) {
    /*var element = document.getElementById("test-display");
    element.innerHTML = "Mouse Outside";*/
  }
  
  function addDiv(e) {
    var element = document.getElementById("div-box");
    element.innerHTML = element.innerHTML;
  }