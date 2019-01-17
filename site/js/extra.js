var dgby=function( id ) { return document.getElementById( id ); };

var rndimg = ['/images/me2.png','/images/me3.png','/images/me4.png','/images/me5.png','/images/me6.png','/images/me7.png','/images/me8.png','/images/me9.png','/images/me10.png']
function iswp(image) {
	var rndnum=Math.floor(Math.random() * rndimg.length);
	console.log(rndimg[rndnum]);
	image.setAttribute('src', rndimg[rndnum]);
}
function iswp2(image) {
	console.log(image.src);
	image.setAttribute('src', '/images/me.png');
}
