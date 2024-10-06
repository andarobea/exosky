let hours, minutes, seconds, degrees, arcminutes, arcseconds;
let DEC, RA;
hours = 12;
minutes = 43;
seconds = 59.4;
degrees = -4;
arcminutes = 43;
arcseconds = 49.3;
DEC = degrees + arcminutes / 60 + arcseconds / 60;
RA = 15 * (hours + minutes / 60 + seconds / 60);
let aladin;
A.init.then(() => {
    aladin = A.aladin('#aladin-lite-div', { fov: 140, projection: "STG", cooFrame: 'equatorial', showCooGridControl: true, showSimbadPointerControl: true, showCooGrid: false });
    aladin.gotoRaDec(RA, DEC);
});

function toggleMenu(){
    const upButton = document.getElementById("upButton");
    const downButton = document.getElementById("downButton");
    const menu = document.getElementById("menu");

    upButton.classList.toggle('hidden');
    downButton.classList.toggle('hidden');
    menu.classList.toggle('hidden');
}