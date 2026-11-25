// Panggung hero (cerita "perjalanan"): di desktop, posisi kursor = detik cerita.
// Kursor ke kanan = maju, ke kiri = mundur, keluar panggung = jalan sendiri lagi. HP / reduced-motion: tetap otomatis.
(function(){
  var pg=document.querySelector('.panggung[data-durasi]');
  if(!pg||!matchMedia('(hover: hover) and (pointer: fine)').matches||matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var DUR=+pg.dataset.durasi, diam;
  var panjang=function(){return pg.getAnimations({subtree:true}).filter(function(a){return a.effect&&a.effect.getTiming().duration>=DUR;});};
  var kaki=function(){var j=pg.querySelector('.pg-aj');return j?j.getAnimations({subtree:true}):[];};
  pg.addEventListener('mousemove',function(e){
    var r=pg.getBoundingClientRect(), p=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width)), t=600+p*(DUR-1200);
    panjang().forEach(function(a){a.pause();a.currentTime=t;});
    kaki().forEach(function(a){a.play();});
    clearTimeout(diam); diam=setTimeout(function(){kaki().forEach(function(a){a.pause();});},150);
  });
  pg.addEventListener('mouseleave',function(){clearTimeout(diam);panjang().concat(kaki()).forEach(function(a){a.play();});});
})();
