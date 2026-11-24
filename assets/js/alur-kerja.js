// Alur kerja: (1) Bobbi barista berjalan mengikuti kursor (desktop) atau scroll (HP), meja terdekat menyala;
// (2) tampilkan kapan mesin demo (repo pipeline) terakhir jalan otomatis.
// Gerak = ganti pose (depan / hadap kiri / hadap kanan) + posisi; kembali menghadap depan saat berhenti.
(function(){
var ak=document.querySelector('.ak');
if(ak){
  var jalur=ak.querySelector('.ak-jalur'),b=ak.querySelector('.ak-barista'),isi=ak.querySelector('.ak-isi');
  var meja=[].slice.call(ak.querySelectorAll('.ak-meja li'));
  var tegak=function(){return matchMedia('(max-width:860px)').matches;};
  var diam=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var akhir=null,t,jarak=0;
  var taruh=function(p){
    p=Math.max(0,Math.min(1,p));
    if(tegak()){b.style.top=p*100+'%';b.style.left='';isi.style.bottom=(100-p*100)+'%';isi.style.right='';}
    else{b.style.left=p*100+'%';b.style.top='';isi.style.right=(100-p*100)+'%';isi.style.bottom='';}
    var k=Math.round(p*(meja.length-1));
    meja.forEach(function(m,i){m.classList.toggle('aktif',i===k);});
    return p;
  };
  var gerak=function(p){
    p=Math.max(0,Math.min(1,p));
    if(akhir!==null&&Math.abs(p-akhir)>0.001){
      b.dataset.pose=p<akhir?'kiri':'kanan';
      jarak+=Math.abs(p-akhir);if(jarak>0.03){jarak=0;b.classList.toggle('langkah');}
    }
    akhir=taruh(p);
    clearTimeout(t);t=setTimeout(function(){b.dataset.pose='depan';b.classList.remove('langkah');},140);
  };
  akhir=taruh(0);
  if(!diam){
    ak.addEventListener('mousemove',function(e){if(tegak())return;var r=jalur.getBoundingClientRect();gerak((e.clientX-r.left)/r.width);});
    addEventListener('scroll',function(){if(!tegak())return;var r=jalur.getBoundingClientRect();gerak((innerHeight*0.5-r.top)/r.height);},{passive:true});
  }
}
document.querySelectorAll('[data-live]').forEach(function(el){
  fetch(el.getAttribute('data-live'),{cache:'no-store'}).then(function(r){return r.ok?r.json():null;}).then(function(d){
    if(d&&d.diperbarui){el.querySelector('b').textContent=d.diperbarui;el.hidden=false;}
  }).catch(function(){});
});
})();
