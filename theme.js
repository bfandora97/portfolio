(function(){
var d=document.documentElement,k='kd-theme';
function saved(){try{return localStorage.getItem(k);}catch(e){return null;}}
function sys(){return matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}
function cur(){return d.getAttribute('data-theme')||sys();}
function paint(){var b=document.getElementById('tg');if(b){var dk=cur()==='dark';b.textContent=dk?'☀':'☾';b.setAttribute('aria-label',dk?'Switch to light mode':'Switch to dark mode');}}
var s=saved();if(s==='dark'||s==='light')d.setAttribute('data-theme',s);
document.addEventListener('DOMContentLoaded',function(){
 var b=document.getElementById('tg');paint();
 if(b)b.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';d.setAttribute('data-theme',n);try{localStorage.setItem(k,n);}catch(e){}paint();dispatchEvent(new Event('themechange'));});
});
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',function(){paint();dispatchEvent(new Event('themechange'));});
function hdr(){var h=document.querySelector('.top');if(h)h.classList.toggle('scrolled',(window.scrollY||d.scrollTop)>40);}
addEventListener('scroll',hdr,{passive:true});document.addEventListener('DOMContentLoaded',hdr);
})();
