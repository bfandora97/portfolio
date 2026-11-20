// Tab gambar + layar penuh di halaman studi kasus
(function(){var v=document.getElementById('views');if(!v)return;var t=[].slice.call(v.querySelectorAll('[role=tab]')),f=[].slice.call(v.querySelectorAll('.shot')),cur=0,lb=document.getElementById('lb'),li=lb.querySelector('img');
function s(n){cur=n;t.forEach(function(b,i){b.classList.toggle('on',i===n);b.setAttribute('aria-selected',i===n?'true':'false');});f.forEach(function(e,i){e.hidden=i!==n;});}
function big(){var im=f[cur].querySelector('img');li.src=im.src;li.alt=im.alt;if(lb.showModal)lb.showModal();}
t.forEach(function(b,i){b.addEventListener('click',function(){s(i);});});
f.forEach(function(e){e.querySelector('img').addEventListener('click',big);});
document.getElementById('fs').addEventListener('click',big);
if(f.length<2){[].forEach.call(lb.querySelectorAll('.nav'),function(b){b.hidden=true;});}
function go(d){var n=(cur+d+f.length)%f.length,im=f[n].querySelector('img');s(n);li.src=im.src;li.alt=im.alt;}
lb.querySelector('.prev').addEventListener('click',function(e){e.stopPropagation();go(-1);});
lb.querySelector('.next').addEventListener('click',function(e){e.stopPropagation();go(1);});
lb.addEventListener('keydown',function(e){if(e.key==='ArrowRight')go(1);else if(e.key==='ArrowLeft')go(-1);});
lb.addEventListener('click',function(){lb.close();});s(0);})();
