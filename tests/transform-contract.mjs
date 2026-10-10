// Run: node tests/transform-contract.mjs
// No dependencies. Contract tests call the actual geometry helpers embedded in index.html.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
const html=readFileSync(new URL("../index.html",import.meta.url),"utf8");
function between(begin,end){
  const a=html.indexOf(begin),b=html.indexOf(end,a+begin.length);
  assert(a>=0&&b>a,`Missing editor helper: ${begin}`);
  return html.slice(a,b);
}
const transforms=between("function frameTransformImage(","function moveDrag(");
const {applyFrame,frameTransformImage}=new Function(transforms+";return {applyFrame,frameTransformImage}")();
const ensureSource=between("function ensureImageRect(","function startDrag(");
const zoomSource=between("function zoomImage(","$(\"quickZoomOut\")");
const zoomImage=new Function(ensureSource+zoomSource+";return zoomImage")();
const approx=(a,b,label)=>assert(Math.abs(a-b)<1e-6,`${label}: expected ${b}, got ${a}`);
const original={x:100,y:120,w:200,h:200,img:{x:50,y:80,w:340,h:400}};
const l={...original,imageRect:{...original.img}};
applyFrame(l,original,{x:80,y:100,w:400,h:400},false);
approx(l.imageRect.w,680,"Whole resize scales source image");
approx(l.imageRect.h,800,"Whole resize preserves source ratio");
approx(l.imageRect.x,-20,"Whole resize transforms image position");
approx(l.imageRect.y,20,"Whole resize transforms image position Y");
// Crop mask resize must not change the underlying source image size.
const previous={...l.imageRect};
const previousMask={x:l.x,y:l.y,w:l.w,h:l.h,img:{...l.imageRect}};
applyFrame(l,previousMask,{x:110,y:130,w:220,h:220},true);
assert.deepEqual(l.imageRect,previous,"Crop-only resize must not modify the image");
const withImage={...l,image:{naturalWidth:500,naturalHeight:400},backing:true,padding:0,imageZoom:1,fit:"cover"};
const maskBefore=[withImage.x,withImage.y,withImage.w,withImage.h];
const sizeBefore=withImage.imageRect.w;
zoomImage(withImage,1.15);
approx(withImage.imageRect.w,sizeBefore*1.15,"Independent zoom grows source image");
assert.deepEqual([withImage.x,withImage.y,withImage.w,withImage.h],maskBefore,"Image zoom must not resize mask");
// Having zoomed/panned the source image, whole-layer resize must preserve composition.
const afterZoom={x:withImage.x,y:withImage.y,w:withImage.w,h:withImage.h,img:{...withImage.imageRect}};
const zoomWidth=withImage.imageRect.w;
applyFrame(withImage,afterZoom,{x:110,y:130,w:440,h:440},false);
approx(withImage.imageRect.w,zoomWidth*2,"After crop, whole resize still scales image and mask together");
assert(html.includes('id="quickTools"')&&html.includes('id="quickMove"')&&html.includes('id="quickCrop"'),"Mode toolbar must exist");
assert(html.includes('id="quickZoomIn"')&&html.includes('id="quickZoomOut"'),"Image zoom controls must exist");
console.log("QRPatch transform contract: 10+ invariants PASS");
