// Alur kerja: tampilkan kapan mesin demo (repo pipeline) terakhir jalan otomatis.
// Gagal dimuat (offline, GitHub lambat) = baris itu tetap tersembunyi, tidak ada error yang terlihat.
(function(){
document.querySelectorAll('[data-live]').forEach(function(el){
  fetch(el.getAttribute('data-live'),{cache:'no-store'}).then(function(r){return r.ok?r.json():null;}).then(function(d){
    if(d&&d.diperbarui){el.querySelector('b').textContent=d.diperbarui;el.hidden=false;}
  }).catch(function(){});
});
})();
