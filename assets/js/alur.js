// Animasi contoh 3 adegan (macro alur). Mulai saat terlihat, berhenti saat tidak terlihat.
// Tombol langkah = lompat ke adegan; tombol jeda/putar. Reduced motion: tidak jalan sendiri, adegan 3 tampil.
(function(){
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var DUR=[0,5200,6000,6500];
[].forEach.call(document.querySelectorAll('[data-alur]'),function(f){
 var bs=[].slice.call(f.querySelectorAll('[data-go]')),pp=f.querySelector('[data-pp]'),s=3,t=null,play=!reduce,vis=false,first=true;
 function set(n){
  s=n;f.setAttribute('data-s',n);f.style.setProperty('--dur',DUR[n]+'ms');
  bs.forEach(function(b){b.setAttribute('aria-pressed',+b.getAttribute('data-go')===n?'true':'false');});
  f.classList.remove('run');void f.offsetWidth;clearTimeout(t);
  if(play&&vis){f.classList.add('run');t=setTimeout(function(){set(n%3+1);},DUR[n]);}
 }
 function upd(){pp.classList.toggle('paused',!play);pp.setAttribute('aria-label',pp.getAttribute(play?'data-jeda':'data-putar'));}
 bs.forEach(function(b){b.addEventListener('click',function(){set(+b.getAttribute('data-go'));});});
 pp.hidden=false;upd();
 pp.addEventListener('click',function(){play=!play;upd();set(play&&s===3?1:s);});
 if(reduce||!('IntersectionObserver' in window)){vis=true;set(3);return;}
 new IntersectionObserver(function(es){es.forEach(function(e){
  vis=e.isIntersecting;
  if(vis){set(first?1:s);first=false;}else{clearTimeout(t);f.classList.remove('run');}
 });},{threshold:.45}).observe(f);
});
})();
