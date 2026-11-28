// Panggung hero (cerita "perjalanan"), khusus desktop: kursor menggeser cerita maju/mundur.
// Posisi kursor DISELARASKAN dengan bilah langkah: kursor di bawah langkah N = adegan N; perpindahan (berjalan) terjadi
// di batas antar-langkah. Cerita MENGEJAR kursor dengan halus (bukan meloncat).
// Kursor keluar = jalan sendiri lagi. HP / reduced-motion: tetap otomatis. Waktu adegan dari data-adegan (gen_karakter.py).
(function(){
  var pg=document.querySelector('.panggung[data-durasi][data-adegan]');
  if(!pg||!matchMedia('(hover: hover) and (pointer: fine)').matches||matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var DUR=+pg.dataset.durasi;
  var ADEGAN=pg.dataset.adegan.split(';').map(function(s){return s.split(',').map(function(n){return n*1000;});});
  var langkah=[].slice.call(pg.querySelectorAll('.pg-langkah li'));
  var target=null, kini=null, raf=null, diam;
  var panjang=function(){return pg.getAnimations({subtree:true}).filter(function(a){return a.effect&&a.effect.getTiming().duration>=DUR;});};
  var kaki=function(){return [].concat.apply([],[].map.call(pg.querySelectorAll('.pg-aj,.pg-bj'),function(e){return e.getAnimations({subtree:true});}));};
  // titik (x 0..1 lebar panggung -> waktu ms), dihitung dari posisi kotak langkah yang sebenarnya
  var titik=function(){
    var r=pg.getBoundingClientRect(), k=[[0,500]];
    langkah.forEach(function(el,i){
      var b=el.getBoundingClientRect(), L=(b.left-r.left)/r.width, R=(b.right-r.left)/r.width, w=R-L, a=ADEGAN[i];
      k.push([L+.08*w, a[0]+100]);                // awal adegan i (kotak langkah i = adegan i)
      k.push([R-.08*w, a[1]-100]);                // akhir adegan; sisanya (di batas) = berjalan ke adegan berikut
    });
    k.push([1,DUR-600]); return k;
  };
  var waktu=function(x){
    var k=titik();
    for(var i=1;i<k.length;i++) if(x<=k[i][0]){var a=k[i-1],b=k[i];return a[1]+(b[1]-a[1])*((x-a[0])/((b[0]-a[0])||1));}
    return k[k.length-1][1];
  };
  var pasang=function(t){panjang().forEach(function(a){a.pause();a.currentTime=t;});};
  var jalan=function(){
    var beda=target-kini;
    kini=Math.abs(beda)<8?target:kini+beda*.09;              // mengejar kursor dengan halus
    if(Math.abs(beda)>=8) pg.classList.toggle('mundur',beda<0); // berbalik saat mundur
    pasang(kini);
    if(kini!==target){raf=requestAnimationFrame(jalan);}
    else{raf=null;clearTimeout(diam);diam=setTimeout(function(){kaki().forEach(function(a){a.pause();});},120);}
  };
  pg.addEventListener('mousemove',function(e){
    var r=pg.getBoundingClientRect();
    target=waktu(Math.max(0,Math.min(1,(e.clientX-r.left)/r.width)));
    if(kini===null){var p=panjang()[0];kini=p?(p.currentTime%DUR):target;}
    clearTimeout(diam); kaki().forEach(function(a){a.play();});
    if(!raf) raf=requestAnimationFrame(jalan);
  });
  pg.addEventListener('mouseleave',function(){
    if(raf) cancelAnimationFrame(raf); raf=null; target=kini=null; clearTimeout(diam);
    pg.classList.remove('mundur'); panjang().concat(kaki()).forEach(function(a){a.play();});
  });
})();
