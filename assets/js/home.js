// Animasi titik di hero (beranda) + efek muncul saat scroll (semua halaman utama: beranda, tentang, layanan, kontak)
(function(){
var c=document.getElementById('dots');if(!c)return; // halaman tanpa hero titik (Tentang, Layanan, Kontak)
var x=c.getContext('2d');
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var tealc,dotc,tr=[14,124,123],dr=[82,96,122];
function hex(h){h=h.replace('#','');return [parseInt(h.substr(0,2),16),parseInt(h.substr(2,2),16),parseInt(h.substr(4,2),16)];}
function readCols(){var s=getComputedStyle(document.documentElement);tealc=s.getPropertyValue("--teal").trim()||"#0e7c7b";dotc=s.getPropertyValue("--dot").trim()||"82,96,122";tr=hex(tealc);dr=dotc.split(',').map(Number);}
var vis=true,running=true,S=22,W,H,dots,cols,rows,barOf,nb,mouse={x:-999,y:-999},t0=performance.now();
function init(){
 var dpr=window.devicePixelRatio||1,r=c.getBoundingClientRect();
 W=r.width;H=r.height;c.width=W*dpr;c.height=H*dpr;x.setTransform(dpr,0,0,dpr,0,0);
 cols=Math.floor(W/S);rows=Math.floor(H/S);
 var ox=(W-(cols-1)*S)/2,oy=(H-(rows-1)*S)/2;dots=[];barOf=[];nb=0;
 for(var i=0;i<cols;i++){barOf[i]=(i%2===1)?nb++:-1;}
 for(i=0;i<cols;i++)for(var j=0;j<rows;j++)dots.push({i:i,j:j,l:false,gx:ox+i*S,gy:oy+j*S,sx:(Math.random()-.5)*260,sy:(Math.random()-.5)*260,dx:0,dy:0,d:i/cols*700+Math.random()*300});
 buildMask();
}
var KD=["1100011","1100110","1101100","1111000","1110000","1111000","1101100","1100110","1100011"],
    DD=["1111100","1100110","1100011","1100011","1100011","1100011","1100011","1100110","1111100"],hasL=false;
function buildMask(){
 if(!dots)return;
 var s=Math.max(1,Math.floor(Math.min((cols-1)/16,(rows-1)/9)));
 hasL=cols>=17&&rows>=10;
 var ox=Math.floor((cols-16*s)/2),oy=Math.floor((rows-9*s)/2);
 for(var n=0;n<dots.length;n++){
  var d=dots[n];d.l=false;d.y=false;
  if(!hasL)continue;
  var u=Math.floor((d.i-ox)/s),v=Math.floor((d.j-oy)/s);
  if(v<0||v>8||u<0||u>15||d.i<ox||d.j<oy)continue;
  var ch=u<7?KD[v].charAt(u):(u>=9?DD[v].charAt(u-9):'0');
  if(ch==='1'){d.l=true;d.y=(v===0);}
 }
}
function barH(k,now){
 var base=.25+.6*k/Math.max(1,nb-1)+Math.sin(k*1.7)*.07;
 return rows*(base+(reduce?0:Math.sin(now/1300+k)*.03));
}
function stt(k,e){
 if(k==='y')return[242,200,17,1,4.2];
 if(k==='t')return[tr[0],tr[1],tr[2],1,3.6];
 if(k==='l')return[tr[0],tr[1],tr[2],1,4.4];
 return[dr[0],dr[1],dr[2],.12+.33*e,2.2];
}
function morph(el){
 if(reduce||!hasL||el<4500)return 0;
 var t=((el-4500)%12000)/1000;
 var v=t<4?0:t<5.2?(t-4)/1.2:t<8.5?1:t<9.7?1-(t-8.5)/1.2:0;
 return v*v*(3-2*v);
}
function frame(now){
 var el=reduce?9999:now-t0,rp=Math.min(1,Math.max(0,(el-1900)/1300)),rise=1-Math.pow(1-rp,3),mo=morph(el);
 x.clearRect(0,0,W,H);
 for(var n=0;n<dots.length;n++){
  var d=dots[n],p=Math.min(1,Math.max(0,(el-d.d)/1300)),e=1-Math.pow(1-p,3);
  var px=d.gx+d.sx*(1-e),py=d.gy+d.sy*(1-e);
  var tx=0,ty=0,mx=px-mouse.x,my=py-mouse.y,dist=Math.hypot(mx,my);
  if(!reduce&&dist<110&&dist>0){var f=(1-dist/110)*16;tx=mx/dist*f;ty=my/dist*f;}
  d.dx+=(tx-d.dx)*.12;d.dy+=(ty-d.dy)*.12;px+=d.dx;py+=d.dy;
  var k=barOf[d.i],inBar=false,top=false;
  if(k>-1){var h=Math.round(barH(k,now)*rise),fb=rows-1-d.j;if(fb<h){inBar=true;top=(fb===h-1);}}
  var A=stt(top?'y':inBar?'t':'b',e),B=stt(d.l?(d.y?'y':'l'):'b',e);
  var q=[0,1,2,3,4].map(function(z){return A[z]+(B[z]-A[z])*mo;});
  x.beginPath();x.fillStyle='rgba('+(q[0]|0)+','+(q[1]|0)+','+(q[2]|0)+','+q[3]+')';x.arc(px,py,q[4],0,6.283);x.fill();
 }
 if(!reduce&&vis)requestAnimationFrame(frame);else running=false;
}
readCols();addEventListener('themechange',function(){readCols();if(reduce)frame(0);});
init();
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(buildMask);
if(reduce){frame(0);}else{requestAnimationFrame(frame);}
if(!reduce&&'IntersectionObserver' in window){new IntersectionObserver(function(es){vis=es[0].isIntersecting;if(vis&&!running){running=true;requestAnimationFrame(frame);}}).observe(c);}
c.addEventListener('mousemove',function(ev){var r=c.getBoundingClientRect();mouse.x=ev.clientX-r.left;mouse.y=ev.clientY-r.top;});
c.addEventListener('mouseleave',function(){mouse.x=mouse.y=-999;});
var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){init();if(reduce)frame(0);},150);});
})();
(function(){
var els=[].slice.call(document.querySelectorAll('.rv'));
if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in');});}
else{var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});},{threshold:.2});els.forEach(function(e){io.observe(e);});}
})();
