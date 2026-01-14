/*! For license information please see chunk.bef0d303a5554c583515.js.LICENSE.txt */
"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[1061],{13066(e,t,o){o.d(t,{AO:()=>u,tp:()=>g});var r=["input","select","textarea","a[href]","button","[tabindex]:not(slot)","audio[controls]","video[controls]",'[contenteditable]:not([contenteditable="false"])',"details>summary:first-of-type","details"],a=r.join(","),i="undefined"==typeof Element,l=i?function(){}:Element.prototype.matches||Element.prototype.msMatchesSelector||Element.prototype.webkitMatchesSelector,s=!i&&Element.prototype.getRootNode?function(e){return e.getRootNode()}:function(e){return e.ownerDocument},n=function(e){return"INPUT"===e.tagName},c=function(e){var t=e.getBoundingClientRect(),o=t.width,r=t.height;return 0===o&&0===r},d=function(e,t){return!(t.disabled||function(e){return n(e)&&"hidden"===e.type}(t)||function(e,t){var o=t.displayCheck,r=t.getShadowRoot;if("hidden"===getComputedStyle(e).visibility)return!0;var a=l.call(e,"details>summary:first-of-type")?e.parentElement:e;if(l.call(a,"details:not([open]) *"))return!0;var i=s(e).host,n=(null==i?void 0:i.ownerDocument.contains(i))||e.ownerDocument.contains(e);if(o&&"full"!==o){if("non-zero-area"===o)return c(e)}else{if("function"==typeof r){for(var d=e;e;){var h=e.parentElement,u=s(e);if(h&&!h.shadowRoot&&!0===r(h))return c(e);e=e.assignedSlot?e.assignedSlot:h||u===e.ownerDocument?h:u.host}e=d}if(n)return!e.getClientRects().length}return!1}(t,e)||function(e){return"DETAILS"===e.tagName&&Array.prototype.slice.apply(e.children).some(function(e){return"SUMMARY"===e.tagName})}(t)||function(e){if(/^(INPUT|BUTTON|SELECT|TEXTAREA)$/.test(e.tagName))for(var t=e.parentElement;t;){if("FIELDSET"===t.tagName&&t.disabled){for(var o=0;o<t.children.length;o++){var r=t.children.item(o);if("LEGEND"===r.tagName)return!!l.call(t,"fieldset[disabled] *")||!r.contains(e)}return!0}t=t.parentElement}return!1}(t))},h=function(e,t){return!(function(e){return function(e){return n(e)&&"radio"===e.type}(e)&&!function(e){if(!e.name)return!0;var t,o=e.form||s(e),r=function(e){return o.querySelectorAll('input[type="radio"][name="'+e+'"]')};if("undefined"!=typeof window&&void 0!==window.CSS&&"function"==typeof window.CSS.escape)t=r(window.CSS.escape(e.name));else try{t=r(e.name)}catch(e){return console.error("Looks like you have a radio button with a name attribute containing invalid CSS selector characters and need the CSS.escape polyfill: %s",e.message),!1}var a=function(e,t){for(var o=0;o<e.length;o++)if(e[o].checked&&e[o].form===t)return e[o]}(t,e.form);return!a||a===e}(e)}(t)||function(e,t){return e.tabIndex<0&&(t||/^(AUDIO|VIDEO|DETAILS)$/.test(e.tagName)||e.isContentEditable)&&isNaN(parseInt(e.getAttribute("tabindex"),10))?0:e.tabIndex}(t)<0||!d(e,t))},u=function(e,t){if(t=t||{},!e)throw new Error("No node provided");return!1!==l.call(e,a)&&h(t,e)},p=r.concat("iframe").join(","),g=function(e,t){if(t=t||{},!e)throw new Error("No node provided");return!1!==l.call(e,p)&&d(t,e)}},51061(e,t,o){o.r(t),o.d(t,{Accordion:()=>Ro,AccordionItem:()=>Lo,Anchor:()=>Xo,AnchoredRegion:()=>Zo,Avatar:()=>or,Badge:()=>lr,Breadcrumb:()=>cr,BreadcrumbItem:()=>ur,Button:()=>br,Card:()=>$r,Checkbox:()=>wr,Combobox:()=>Vr,DataGrid:()=>Ir,DataGridCell:()=>jr,DataGridRow:()=>Or,DateField:()=>Gr,DelegatesARIAToolbar:()=>Si,DesignSystemProvider:()=>Zr,Dialog:()=>oa,DirectionalStyleSheetBehavior:()=>Qo,Disclosure:()=>ia,Divider:()=>na,FoundationToolbar:()=>Ci,Listbox:()=>da,Menu:()=>pa,MenuItem:()=>ma,NumberField:()=>$a,Option:()=>ka,PaletteRGB:()=>b,Picker:()=>Ui,PickerList:()=>Ji,PickerListItem:()=>el,PickerMenu:()=>Xi,PickerMenuOption:()=>Yi,Progress:()=>Sa,ProgressRing:()=>Va,Radio:()=>Ha,RadioGroup:()=>Oa,Search:()=>Pa,Select:()=>Ma,Skeleton:()=>Wa,Slider:()=>Ya,SliderLabel:()=>ti,StandardLuminance:()=>n,SwatchRGB:()=>i,Switch:()=>ai,Tab:()=>di,TabPanel:()=>si,Tabs:()=>pi,TextArea:()=>mi,TextField:()=>$i,Toolbar:()=>Fi,Tooltip:()=>Ti,TreeItem:()=>Ii,TreeView:()=>Pi,accentColor:()=>je,accentFillActive:()=>Je,accentFillActiveDelta:()=>re,accentFillFocus:()=>Qe,accentFillFocusDelta:()=>ae,accentFillHover:()=>Ze,accentFillHoverDelta:()=>oe,accentFillRecipe:()=>Ke,accentFillRest:()=>Ye,accentFillRestDelta:()=>te,accentForegroundActive:()=>gt,accentForegroundActiveDelta:()=>se,accentForegroundFocus:()=>bt,accentForegroundFocusDelta:()=>ne,accentForegroundHover:()=>pt,accentForegroundHoverDelta:()=>le,accentForegroundRecipe:()=>ht,accentForegroundRest:()=>ut,accentForegroundRestDelta:()=>ie,accentPalette:()=>Le,accordionItemStyles:()=>jo,accordionStyles:()=>Bo,addJupyterLabThemeChangeListener:()=>Fo,allComponents:()=>ol,anchorStyles:()=>qo,anchoredRegionStyles:()=>Yo,applyJupyterTheme:()=>To,avatarStyles:()=>tr,badgeStyles:()=>ir,baseHeightMultiplier:()=>F,baseHorizontalSpacingMultiplier:()=>D,baseLayerLuminance:()=>V,bodyFont:()=>S,breadcrumbItemStyles:()=>hr,breadcrumbStyles:()=>nr,buttonStyles:()=>gr,cardStyles:()=>vr,checkboxStyles:()=>yr,checkboxTemplate:()=>kr,comboboxStyles:()=>Dr,controlCornerRadius:()=>T,dataGridCellStyles:()=>Hr,dataGridRowStyles:()=>Br,dataGridStyles:()=>zr,dateFieldStyles:()=>Wr,dateFieldTemplate:()=>Ur,density:()=>z,designSystemProviderStyles:()=>Qr,designSystemProviderTemplate:()=>Jr,designUnit:()=>B,dialogStyles:()=>ta,direction:()=>j,disabledOpacity:()=>L,disclosureStyles:()=>aa,dividerStyles:()=>sa,elementScale:()=>H,errorColor:()=>eo,errorFillActive:()=>io,errorFillFocus:()=>lo,errorFillHover:()=>ao,errorFillRecipe:()=>oo,errorFillRest:()=>ro,errorForegroundActive:()=>ko,errorForegroundFocus:()=>wo,errorForegroundHover:()=>yo,errorForegroundRecipe:()=>$o,errorForegroundRest:()=>xo,errorPalette:()=>to,fillColor:()=>qe,focusStrokeInner:()=>Et,focusStrokeInnerRecipe:()=>Pt,focusStrokeOuter:()=>At,focusStrokeOuterRecipe:()=>Nt,focusStrokeWidth:()=>R,foregroundOnAccentActive:()=>at,foregroundOnAccentActiveLarge:()=>ct,foregroundOnAccentFocus:()=>it,foregroundOnAccentFocusLarge:()=>dt,foregroundOnAccentHover:()=>rt,foregroundOnAccentHoverLarge:()=>nt,foregroundOnAccentLargeRecipe:()=>lt,foregroundOnAccentRecipe:()=>tt,foregroundOnAccentRest:()=>ot,foregroundOnAccentRestLarge:()=>st,foregroundOnErrorActive:()=>uo,foregroundOnErrorActiveLarge:()=>fo,foregroundOnErrorFocus:()=>po,foregroundOnErrorFocusLarge:()=>vo,foregroundOnErrorHover:()=>ho,foregroundOnErrorHoverLarge:()=>mo,foregroundOnErrorLargeRecipe:()=>go,foregroundOnErrorRecipe:()=>no,foregroundOnErrorRest:()=>co,foregroundOnErrorRestLarge:()=>bo,heightNumberAsToken:()=>Qt,horizontalSliderLabelStyles:()=>Ja,imgTemplate:()=>rr,isDark:()=>d,jpAccordion:()=>Io,jpAccordionItem:()=>Oo,jpAnchor:()=>Ko,jpAnchoredRegion:()=>Jo,jpAvatar:()=>ar,jpBadge:()=>sr,jpBreadcrumb:()=>dr,jpBreadcrumbItem:()=>pr,jpButton:()=>mr,jpCard:()=>xr,jpCheckbox:()=>Cr,jpCombobox:()=>Tr,jpDataGrid:()=>Nr,jpDataGridCell:()=>Lr,jpDataGridRow:()=>Rr,jpDateField:()=>qr,jpDesignSystemProvider:()=>ea,jpDialog:()=>ra,jpDisclosure:()=>la,jpDivider:()=>ca,jpListbox:()=>ha,jpMenu:()=>ga,jpMenuItem:()=>fa,jpNumberField:()=>xa,jpOption:()=>wa,jpPicker:()=>qi,jpPickerList:()=>Qi,jpPickerListItem:()=>tl,jpPickerMenu:()=>Ki,jpPickerMenuOption:()=>Zi,jpProgress:()=>Fa,jpProgressRing:()=>Ta,jpRadio:()=>ja,jpRadioGroup:()=>Ra,jpSearch:()=>Ea,jpSelect:()=>Ga,jpSkeleton:()=>Ua,jpSlider:()=>Za,jpSliderLabel:()=>oi,jpSwitch:()=>ii,jpTab:()=>hi,jpTabPanel:()=>ni,jpTabs:()=>gi,jpTextArea:()=>fi,jpTextField:()=>xi,jpToolbar:()=>Di,jpTooltip:()=>zi,jpTreeItem:()=>Ni,jpTreeView:()=>Ei,listboxStyles:()=>Sr,menuItemStyles:()=>ba,menuStyles:()=>ua,neutralColor:()=>Be,neutralFillActive:()=>$t,neutralFillActiveDelta:()=>he,neutralFillFocus:()=>xt,neutralFillFocusDelta:()=>ue,neutralFillHover:()=>vt,neutralFillHoverDelta:()=>de,neutralFillInputActive:()=>Ct,neutralFillInputActiveDelta:()=>be,neutralFillInputFocus:()=>St,neutralFillInputFocusDelta:()=>me,neutralFillInputHover:()=>wt,neutralFillInputHoverDelta:()=>ge,neutralFillInputRecipe:()=>yt,neutralFillInputRest:()=>kt,neutralFillInputRestDelta:()=>pe,neutralFillLayerRecipe:()=>Rt,neutralFillLayerRest:()=>It,neutralFillLayerRestDelta:()=>Se,neutralFillRecipe:()=>mt,neutralFillRest:()=>ft,neutralFillRestDelta:()=>ce,neutralFillStealthActive:()=>Tt,neutralFillStealthActiveDelta:()=>$e,neutralFillStealthFocus:()=>zt,neutralFillStealthFocusDelta:()=>xe,neutralFillStealthHover:()=>Vt,neutralFillStealthHoverDelta:()=>ve,neutralFillStealthRecipe:()=>Ft,neutralFillStealthRest:()=>Dt,neutralFillStealthRestDelta:()=>fe,neutralFillStrongActive:()=>Lt,neutralFillStrongActiveDelta:()=>we,neutralFillStrongFocus:()=>Ot,neutralFillStrongFocusDelta:()=>Ce,neutralFillStrongHover:()=>jt,neutralFillStrongHoverDelta:()=>ke,neutralFillStrongRecipe:()=>Bt,neutralFillStrongRest:()=>Ht,neutralFillStrongRestDelta:()=>ye,neutralForegroundHint:()=>Gt,neutralForegroundHintRecipe:()=>Mt,neutralForegroundRecipe:()=>_t,neutralForegroundRest:()=>Wt,neutralLayer1:()=>Pe,neutralLayer1Recipe:()=>Ae,neutralLayer2:()=>Me,neutralLayer2Recipe:()=>Ee,neutralLayer3:()=>_e,neutralLayer3Recipe:()=>Ge,neutralLayer4:()=>Ue,neutralLayer4Recipe:()=>We,neutralLayerCardContainer:()=>Re,neutralLayerCardContainerRecipe:()=>Oe,neutralLayerFloating:()=>Ne,neutralLayerFloatingRecipe:()=>Ie,neutralPalette:()=>He,neutralStrokeActive:()=>Kt,neutralStrokeActiveDelta:()=>Ve,neutralStrokeDividerRecipe:()=>Zt,neutralStrokeDividerRest:()=>Jt,neutralStrokeDividerRestDelta:()=>ze,neutralStrokeFocus:()=>Yt,neutralStrokeFocusDelta:()=>Te,neutralStrokeHover:()=>Xt,neutralStrokeHoverDelta:()=>De,neutralStrokeRecipe:()=>Ut,neutralStrokeRest:()=>qt,neutralStrokeRestDelta:()=>Fe,numberFieldStyles:()=>va,optionStyles:()=>ya,pickerListItemStyles:()=>Wi,pickerMenuOptionStyles:()=>_i,pickerMenuStyles:()=>Gi,pickerStyles:()=>Mi,progressRingStyles:()=>Da,progressStyles:()=>Ca,provideJupyterDesignSystem:()=>rl,radioGroupStyles:()=>La,radioStyles:()=>za,radioTemplate:()=>Ba,searchStyles:()=>Aa,selectStyles:()=>Fr,skeletonStyles:()=>_a,sliderLabelStyles:()=>ei,sliderStyles:()=>Ka,strokeWidth:()=>O,switchStyles:()=>ri,tabPanelStyles:()=>li,tabStyles:()=>ci,tabsStyles:()=>ui,textAreaStyles:()=>bi,textFieldStyles:()=>vi,toolbarStyles:()=>ki,tooltipStyles:()=>Vi,treeItemStyles:()=>Ri,treeViewStyles:()=>Ai,typeRampBaseFontSize:()=>I,typeRampBaseLineHeight:()=>N,typeRampMinus1FontSize:()=>A,typeRampMinus1LineHeight:()=>P,typeRampMinus2FontSize:()=>E,typeRampMinus2LineHeight:()=>M,typeRampPlus1FontSize:()=>G,typeRampPlus1LineHeight:()=>_,typeRampPlus2FontSize:()=>W,typeRampPlus2LineHeight:()=>U,typeRampPlus3FontSize:()=>q,typeRampPlus3LineHeight:()=>X,typeRampPlus4FontSize:()=>K,typeRampPlus4LineHeight:()=>Y,typeRampPlus5FontSize:()=>Z,typeRampPlus5LineHeight:()=>J,typeRampPlus6FontSize:()=>Q,typeRampPlus6LineHeight:()=>ee,verticalSliderLabelStyles:()=>Qa});var r=o(35284);function a(e,t){const o=e.relativeLuminance>t.relativeLuminance?e:t,r=e.relativeLuminance>t.relativeLuminance?t:e;return(o.relativeLuminance+.05)/(r.relativeLuminance+.05)}const i=Object.freeze({create:(e,t,o)=>new l(e,t,o),from:e=>new l(e.r,e.g,e.b)});class l extends r.ColorRGBA64{constructor(e,t,o){super(e,t,o,1),this.toColorString=this.toStringHexRGB,this.contrast=a.bind(null,this),this.createCSS=this.toColorString,this.relativeLuminance=(0,r.rgbToRelativeLuminance)(this)}static fromObject(e){return new l(e.r,e.g,e.b)}}function s(e){return i.create(e,e,e)}const n={LightMode:1,DarkMode:.23},c=(-.1+Math.sqrt(.21))/2;function d(e){return e.relativeLuminance<=c}var h=o(95838),u=o(48601);function p(e,t,o=0,r=e.length-1){if(r===o)return e[o];const a=Math.floor((r-o)/2)+o;return t(e[a])?p(e,t,o,a):p(e,t,a+1,r)}function g(e){return d(e)?-1:1}const b=Object.freeze({create:function(e,t,o){return"number"==typeof e?b.from(i.create(e,t,o)):b.from(e)},from:function(e){return function(e){const t={r:0,g:0,b:0,toColorString:()=>"",contrast:()=>0,relativeLuminance:0};for(const o in t)if(typeof t[o]!=typeof e[o])return!1;return!0}(e)?m.from(e):m.from(i.create(e.r,e.g,e.b))}});class m{constructor(e,t){this.closestIndexCache=new Map,this.source=e,this.swatches=t,this.reversedSwatches=Object.freeze([...this.swatches].reverse()),this.lastIndex=this.swatches.length-1}colorContrast(e,t,o,r){void 0===o&&(o=this.closestIndexOf(e));let i=this.swatches;const l=this.lastIndex;let s=o;return void 0===r&&(r=g(e)),-1===r&&(i=this.reversedSwatches,s=l-s),p(i,o=>a(e,o)>=t,s,l)}get(e){return this.swatches[e]||this.swatches[(0,r.clamp)(e,0,this.lastIndex)]}closestIndexOf(e){if(this.closestIndexCache.has(e.relativeLuminance))return this.closestIndexCache.get(e.relativeLuminance);let t=this.swatches.indexOf(e);if(-1!==t)return this.closestIndexCache.set(e.relativeLuminance,t),t;const o=this.swatches.reduce((t,o)=>Math.abs(o.relativeLuminance-e.relativeLuminance)<Math.abs(t.relativeLuminance-e.relativeLuminance)?o:t);return t=this.swatches.indexOf(o),this.closestIndexCache.set(e.relativeLuminance,t),t}static from(e){return new m(e,Object.freeze(new r.ComponentStateColorPalette({baseColor:r.ColorRGBA64.fromObject(e)}).palette.map(e=>{const t=(0,r.parseColorHexRGB)(e.toStringHexRGB());return i.create(t.r,t.g,t.b)})))}}const f=i.create(1,1,1),v=i.create(0,0,0),$=i.from((0,r.parseColorHexRGB)("#808080")),x=i.from((0,r.parseColorHexRGB)("#DA1A5F")),y=i.from((0,r.parseColorHexRGB)("#D32F2F"));function k(e,t,o,r,a,i){return Math.max(e.closestIndexOf(s(t))+o,r,a,i)}const{create:w}=h.DesignToken;function C(e){return h.DesignToken.create({name:e,cssCustomPropertyName:null})}const S=w("body-font").withDefault('aktiv-grotesk, "Segoe UI", Arial, Helvetica, sans-serif'),F=w("base-height-multiplier").withDefault(10),D=w("base-horizontal-spacing-multiplier").withDefault(3),V=w("base-layer-luminance").withDefault(n.DarkMode),T=w("control-corner-radius").withDefault(4),z=w("density").withDefault(0),B=w("design-unit").withDefault(4),H=w("element-scale").withDefault(0),j=w("direction").withDefault(u.Direction.ltr),L=w("disabled-opacity").withDefault(.4),O=w("stroke-width").withDefault(1),R=w("focus-stroke-width").withDefault(2),I=w("type-ramp-base-font-size").withDefault("14px"),N=w("type-ramp-base-line-height").withDefault("20px"),A=w("type-ramp-minus-1-font-size").withDefault("12px"),P=w("type-ramp-minus-1-line-height").withDefault("16px"),E=w("type-ramp-minus-2-font-size").withDefault("10px"),M=w("type-ramp-minus-2-line-height").withDefault("16px"),G=w("type-ramp-plus-1-font-size").withDefault("16px"),_=w("type-ramp-plus-1-line-height").withDefault("24px"),W=w("type-ramp-plus-2-font-size").withDefault("20px"),U=w("type-ramp-plus-2-line-height").withDefault("28px"),q=w("type-ramp-plus-3-font-size").withDefault("28px"),X=w("type-ramp-plus-3-line-height").withDefault("36px"),K=w("type-ramp-plus-4-font-size").withDefault("34px"),Y=w("type-ramp-plus-4-line-height").withDefault("44px"),Z=w("type-ramp-plus-5-font-size").withDefault("46px"),J=w("type-ramp-plus-5-line-height").withDefault("56px"),Q=w("type-ramp-plus-6-font-size").withDefault("60px"),ee=w("type-ramp-plus-6-line-height").withDefault("72px"),te=C("accent-fill-rest-delta").withDefault(0),oe=C("accent-fill-hover-delta").withDefault(4),re=C("accent-fill-active-delta").withDefault(-5),ae=C("accent-fill-focus-delta").withDefault(0),ie=C("accent-foreground-rest-delta").withDefault(0),le=C("accent-foreground-hover-delta").withDefault(6),se=C("accent-foreground-active-delta").withDefault(-4),ne=C("accent-foreground-focus-delta").withDefault(0),ce=C("neutral-fill-rest-delta").withDefault(7),de=C("neutral-fill-hover-delta").withDefault(10),he=C("neutral-fill-active-delta").withDefault(5),ue=C("neutral-fill-focus-delta").withDefault(0),pe=C("neutral-fill-input-rest-delta").withDefault(0),ge=C("neutral-fill-input-hover-delta").withDefault(0),be=C("neutral-fill-input-active-delta").withDefault(0),me=C("neutral-fill-input-focus-delta").withDefault(0),fe=C("neutral-fill-stealth-rest-delta").withDefault(0),ve=C("neutral-fill-stealth-hover-delta").withDefault(5),$e=C("neutral-fill-stealth-active-delta").withDefault(3),xe=C("neutral-fill-stealth-focus-delta").withDefault(0),ye=C("neutral-fill-strong-rest-delta").withDefault(0),ke=C("neutral-fill-strong-hover-delta").withDefault(8),we=C("neutral-fill-strong-active-delta").withDefault(-5),Ce=C("neutral-fill-strong-focus-delta").withDefault(0),Se=C("neutral-fill-layer-rest-delta").withDefault(3),Fe=C("neutral-stroke-rest-delta").withDefault(25),De=C("neutral-stroke-hover-delta").withDefault(40),Ve=C("neutral-stroke-active-delta").withDefault(16),Te=C("neutral-stroke-focus-delta").withDefault(25),ze=C("neutral-stroke-divider-rest-delta").withDefault(8),Be=w("neutral-color").withDefault($),He=C("neutral-palette").withDefault(e=>b.from(Be.getValueFor(e))),je=w("accent-color").withDefault(x),Le=C("accent-palette").withDefault(e=>b.from(je.getValueFor(e))),Oe=C("neutral-layer-card-container-recipe").withDefault({evaluate:e=>{return t=He.getValueFor(e),o=V.getValueFor(e),r=Se.getValueFor(e),t.get(t.closestIndexOf(s(o))+r);var t,o,r}}),Re=w("neutral-layer-card-container").withDefault(e=>Oe.getValueFor(e).evaluate(e)),Ie=C("neutral-layer-floating-recipe").withDefault({evaluate:e=>function(e,t,o){const r=e.closestIndexOf(s(t))-o;return e.get(r-o)}(He.getValueFor(e),V.getValueFor(e),Se.getValueFor(e))}),Ne=w("neutral-layer-floating").withDefault(e=>Ie.getValueFor(e).evaluate(e)),Ae=C("neutral-layer-1-recipe").withDefault({evaluate:e=>function(e,t){return e.get(e.closestIndexOf(s(t)))}(He.getValueFor(e),V.getValueFor(e))}),Pe=w("neutral-layer-1").withDefault(e=>Ae.getValueFor(e).evaluate(e)),Ee=C("neutral-layer-2-recipe").withDefault({evaluate:e=>{return t=He.getValueFor(e),o=V.getValueFor(e),r=Se.getValueFor(e),a=ce.getValueFor(e),i=de.getValueFor(e),l=he.getValueFor(e),t.get(k(t,o,r,a,i,l));var t,o,r,a,i,l}}),Me=w("neutral-layer-2").withDefault(e=>Ee.getValueFor(e).evaluate(e)),Ge=C("neutral-layer-3-recipe").withDefault({evaluate:e=>{return t=He.getValueFor(e),o=V.getValueFor(e),r=Se.getValueFor(e),a=ce.getValueFor(e),i=de.getValueFor(e),l=he.getValueFor(e),t.get(k(t,o,r,a,i,l)+r);var t,o,r,a,i,l}}),_e=w("neutral-layer-3").withDefault(e=>Ge.getValueFor(e).evaluate(e)),We=C("neutral-layer-4-recipe").withDefault({evaluate:e=>{return t=He.getValueFor(e),o=V.getValueFor(e),r=Se.getValueFor(e),a=ce.getValueFor(e),i=de.getValueFor(e),l=he.getValueFor(e),t.get(k(t,o,r,a,i,l)+2*r);var t,o,r,a,i,l}}),Ue=w("neutral-layer-4").withDefault(e=>We.getValueFor(e).evaluate(e)),qe=w("fill-color").withDefault(e=>Pe.getValueFor(e));var Xe;!function(e){e[e.normal=4.5]="normal",e[e.large=7]="large"}(Xe||(Xe={}));const Ke=w({name:"accent-fill-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>function(e,t,o,r,a,i,l,s,n){const c=e.source,d=t.closestIndexOf(o)>=Math.max(l,s,n)?-1:1,h=e.closestIndexOf(c),u=h+-1*d*r,p=u+d*a,g=u+d*i;return{rest:e.get(u),hover:e.get(h),active:e.get(p),focus:e.get(g)}}(Le.getValueFor(e),He.getValueFor(e),t||qe.getValueFor(e),oe.getValueFor(e),re.getValueFor(e),ae.getValueFor(e),ce.getValueFor(e),de.getValueFor(e),he.getValueFor(e))}),Ye=w("accent-fill-rest").withDefault(e=>Ke.getValueFor(e).evaluate(e).rest),Ze=w("accent-fill-hover").withDefault(e=>Ke.getValueFor(e).evaluate(e).hover),Je=w("accent-fill-active").withDefault(e=>Ke.getValueFor(e).evaluate(e).active),Qe=w("accent-fill-focus").withDefault(e=>Ke.getValueFor(e).evaluate(e).focus),et=e=>(t,o)=>function(e,t){return e.contrast(f)>=t?f:v}(o||Ye.getValueFor(t),e),tt=C("foreground-on-accent-recipe").withDefault({evaluate:(e,t)=>et(Xe.normal)(e,t)}),ot=w("foreground-on-accent-rest").withDefault(e=>tt.getValueFor(e).evaluate(e,Ye.getValueFor(e))),rt=w("foreground-on-accent-hover").withDefault(e=>tt.getValueFor(e).evaluate(e,Ze.getValueFor(e))),at=w("foreground-on-accent-active").withDefault(e=>tt.getValueFor(e).evaluate(e,Je.getValueFor(e))),it=w("foreground-on-accent-focus").withDefault(e=>tt.getValueFor(e).evaluate(e,Qe.getValueFor(e))),lt=C("foreground-on-accent-large-recipe").withDefault({evaluate:(e,t)=>et(Xe.large)(e,t)}),st=w("foreground-on-accent-rest-large").withDefault(e=>lt.getValueFor(e).evaluate(e,Ye.getValueFor(e))),nt=w("foreground-on-accent-hover-large").withDefault(e=>lt.getValueFor(e).evaluate(e,Ze.getValueFor(e))),ct=w("foreground-on-accent-active-large").withDefault(e=>lt.getValueFor(e).evaluate(e,Je.getValueFor(e))),dt=w("foreground-on-accent-focus-large").withDefault(e=>lt.getValueFor(e).evaluate(e,Qe.getValueFor(e))),ht=w({name:"accent-foreground-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>(e=>(t,o)=>function(e,t,o,r,a,i,l){const s=e.source,n=e.closestIndexOf(s),c=g(t),d=n+(1===c?Math.min(r,a):Math.max(c*r,c*a)),h=e.colorContrast(t,o,d,c),u=e.closestIndexOf(h),p=u+c*Math.abs(r-a);let b,m;return(1===c?r<a:c*r>c*a)?(b=u,m=p):(b=p,m=u),{rest:e.get(b),hover:e.get(m),active:e.get(b+c*i),focus:e.get(b+c*l)}}(Le.getValueFor(t),o||qe.getValueFor(t),e,ie.getValueFor(t),le.getValueFor(t),se.getValueFor(t),ne.getValueFor(t)))(Xe.normal)(e,t)}),ut=w("accent-foreground-rest").withDefault(e=>ht.getValueFor(e).evaluate(e).rest),pt=w("accent-foreground-hover").withDefault(e=>ht.getValueFor(e).evaluate(e).hover),gt=w("accent-foreground-active").withDefault(e=>ht.getValueFor(e).evaluate(e).active),bt=w("accent-foreground-focus").withDefault(e=>ht.getValueFor(e).evaluate(e).focus),mt=w({name:"neutral-fill-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>function(e,t,o,r,a,i){const l=e.closestIndexOf(t),s=l>=Math.max(o,r,a,i)?-1:1;return{rest:e.get(l+s*o),hover:e.get(l+s*r),active:e.get(l+s*a),focus:e.get(l+s*i)}}(He.getValueFor(e),t||qe.getValueFor(e),ce.getValueFor(e),de.getValueFor(e),he.getValueFor(e),ue.getValueFor(e))}),ft=w("neutral-fill-rest").withDefault(e=>mt.getValueFor(e).evaluate(e).rest),vt=w("neutral-fill-hover").withDefault(e=>mt.getValueFor(e).evaluate(e).hover),$t=w("neutral-fill-active").withDefault(e=>mt.getValueFor(e).evaluate(e).active),xt=w("neutral-fill-focus").withDefault(e=>mt.getValueFor(e).evaluate(e).focus),yt=w({name:"neutral-fill-input-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>function(e,t,o,r,a,i){const l=g(t),s=e.closestIndexOf(t);return{rest:e.get(s-l*o),hover:e.get(s-l*r),active:e.get(s-l*a),focus:e.get(s-l*i)}}(He.getValueFor(e),t||qe.getValueFor(e),pe.getValueFor(e),ge.getValueFor(e),be.getValueFor(e),me.getValueFor(e))}),kt=w("neutral-fill-input-rest").withDefault(e=>yt.getValueFor(e).evaluate(e).rest),wt=w("neutral-fill-input-hover").withDefault(e=>yt.getValueFor(e).evaluate(e).hover),Ct=w("neutral-fill-input-active").withDefault(e=>yt.getValueFor(e).evaluate(e).active),St=w("neutral-fill-input-focus").withDefault(e=>yt.getValueFor(e).evaluate(e).focus),Ft=w({name:"neutral-fill-stealth-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>function(e,t,o,r,a,i,l,s,n,c){const d=Math.max(o,r,a,i,l,s,n,c),h=e.closestIndexOf(t),u=h>=d?-1:1;return{rest:e.get(h+u*o),hover:e.get(h+u*r),active:e.get(h+u*a),focus:e.get(h+u*i)}}(He.getValueFor(e),t||qe.getValueFor(e),fe.getValueFor(e),ve.getValueFor(e),$e.getValueFor(e),xe.getValueFor(e),ce.getValueFor(e),de.getValueFor(e),he.getValueFor(e),ue.getValueFor(e))}),Dt=w("neutral-fill-stealth-rest").withDefault(e=>Ft.getValueFor(e).evaluate(e).rest),Vt=w("neutral-fill-stealth-hover").withDefault(e=>Ft.getValueFor(e).evaluate(e).hover),Tt=w("neutral-fill-stealth-active").withDefault(e=>Ft.getValueFor(e).evaluate(e).active),zt=w("neutral-fill-stealth-focus").withDefault(e=>Ft.getValueFor(e).evaluate(e).focus),Bt=w({name:"neutral-fill-strong-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>function(e,t,o,r,a,i){const l=g(t),s=e.closestIndexOf(e.colorContrast(t,4.5)),n=s+l*Math.abs(o-r);let c,d;return(1===l?o<r:l*o>l*r)?(c=s,d=n):(c=n,d=s),{rest:e.get(c),hover:e.get(d),active:e.get(c+l*a),focus:e.get(c+l*i)}}(He.getValueFor(e),t||qe.getValueFor(e),ye.getValueFor(e),ke.getValueFor(e),we.getValueFor(e),Ce.getValueFor(e))}),Ht=w("neutral-fill-strong-rest").withDefault(e=>Bt.getValueFor(e).evaluate(e).rest),jt=w("neutral-fill-strong-hover").withDefault(e=>Bt.getValueFor(e).evaluate(e).hover),Lt=w("neutral-fill-strong-active").withDefault(e=>Bt.getValueFor(e).evaluate(e).active),Ot=w("neutral-fill-strong-focus").withDefault(e=>Bt.getValueFor(e).evaluate(e).focus),Rt=C("neutral-fill-layer-recipe").withDefault({evaluate:(e,t)=>function(e,t,o){const r=e.closestIndexOf(t);return e.get(r-(r<o?-1*o:o))}(He.getValueFor(e),t||qe.getValueFor(e),Se.getValueFor(e))}),It=w("neutral-fill-layer-rest").withDefault(e=>Rt.getValueFor(e).evaluate(e)),Nt=C("focus-stroke-outer-recipe").withDefault({evaluate:e=>{return t=He.getValueFor(e),o=qe.getValueFor(e),t.colorContrast(o,3.5);var t,o}}),At=w("focus-stroke-outer").withDefault(e=>Nt.getValueFor(e).evaluate(e)),Pt=C("focus-stroke-inner-recipe").withDefault({evaluate:e=>{return t=Le.getValueFor(e),o=qe.getValueFor(e),r=At.getValueFor(e),t.colorContrast(r,3.5,t.closestIndexOf(t.source),-1*g(o));var t,o,r}}),Et=w("focus-stroke-inner").withDefault(e=>Pt.getValueFor(e).evaluate(e)),Mt=C("neutral-foreground-hint-recipe").withDefault({evaluate:e=>{return t=He.getValueFor(e),o=qe.getValueFor(e),t.colorContrast(o,4.5);var t,o}}),Gt=w("neutral-foreground-hint").withDefault(e=>Mt.getValueFor(e).evaluate(e)),_t=C("neutral-foreground-recipe").withDefault({evaluate:e=>{return t=He.getValueFor(e),o=qe.getValueFor(e),t.colorContrast(o,14);var t,o}}),Wt=w("neutral-foreground-rest").withDefault(e=>_t.getValueFor(e).evaluate(e)),Ut=w({name:"neutral-stroke-recipe",cssCustomPropertyName:null}).withDefault({evaluate:e=>function(e,t,o,r,a,i){const l=e.closestIndexOf(t),s=g(t),n=l+s*o,c=n+s*(r-o),d=n+s*(a-o),h=n+s*(i-o);return{rest:e.get(n),hover:e.get(c),active:e.get(d),focus:e.get(h)}}(He.getValueFor(e),qe.getValueFor(e),Fe.getValueFor(e),De.getValueFor(e),Ve.getValueFor(e),Te.getValueFor(e))}),qt=w("neutral-stroke-rest").withDefault(e=>Ut.getValueFor(e).evaluate(e).rest),Xt=w("neutral-stroke-hover").withDefault(e=>Ut.getValueFor(e).evaluate(e).hover),Kt=w("neutral-stroke-active").withDefault(e=>Ut.getValueFor(e).evaluate(e).active),Yt=w("neutral-stroke-focus").withDefault(e=>Ut.getValueFor(e).evaluate(e).focus),Zt=C("neutral-stroke-divider-recipe").withDefault({evaluate:(e,t)=>function(e,t,o){return e.get(e.closestIndexOf(t)+g(t)*o)}(He.getValueFor(e),t||qe.getValueFor(e),ze.getValueFor(e))}),Jt=w("neutral-stroke-divider-rest").withDefault(e=>Zt.getValueFor(e).evaluate(e)),Qt=h.DesignToken.create({name:"height-number",cssCustomPropertyName:null}).withDefault(e=>(F.getValueFor(e)+z.getValueFor(e))*B.getValueFor(e)),eo=w("error-color").withDefault(y),to=C("error-palette").withDefault(e=>b.from(eo.getValueFor(e))),oo=w({name:"error-fill-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>function(e,t,o,r,a,i,l,s,n){const c=e.source,d=t.closestIndexOf(o)>=Math.max(l,s,n)?-1:1,h=e.closestIndexOf(c),u=h+-1*d*r,p=u+d*a,g=u+d*i;return{rest:e.get(u),hover:e.get(h),active:e.get(p),focus:e.get(g)}}(to.getValueFor(e),He.getValueFor(e),t||qe.getValueFor(e),oe.getValueFor(e),re.getValueFor(e),ae.getValueFor(e),ce.getValueFor(e),de.getValueFor(e),he.getValueFor(e))}),ro=w("error-fill-rest").withDefault(e=>oo.getValueFor(e).evaluate(e).rest),ao=w("error-fill-hover").withDefault(e=>oo.getValueFor(e).evaluate(e).hover),io=w("error-fill-active").withDefault(e=>oo.getValueFor(e).evaluate(e).active),lo=w("error-fill-focus").withDefault(e=>oo.getValueFor(e).evaluate(e).focus),so=e=>(t,o)=>function(e,t){return e.contrast(f)>=t?f:v}(o||ro.getValueFor(t),e),no=w({name:"foreground-on-error-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>so(Xe.normal)(e,t)}),co=w("foreground-on-error-rest").withDefault(e=>no.getValueFor(e).evaluate(e,ro.getValueFor(e))),ho=w("foreground-on-error-hover").withDefault(e=>no.getValueFor(e).evaluate(e,ao.getValueFor(e))),uo=w("foreground-on-error-active").withDefault(e=>no.getValueFor(e).evaluate(e,io.getValueFor(e))),po=w("foreground-on-error-focus").withDefault(e=>no.getValueFor(e).evaluate(e,lo.getValueFor(e))),go=w({name:"foreground-on-error-large-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>so(Xe.large)(e,t)}),bo=w("foreground-on-error-rest-large").withDefault(e=>go.getValueFor(e).evaluate(e,ro.getValueFor(e))),mo=w("foreground-on-error-hover-large").withDefault(e=>go.getValueFor(e).evaluate(e,ao.getValueFor(e))),fo=w("foreground-on-error-active-large").withDefault(e=>go.getValueFor(e).evaluate(e,io.getValueFor(e))),vo=w("foreground-on-error-focus-large").withDefault(e=>go.getValueFor(e).evaluate(e,lo.getValueFor(e))),$o=w({name:"error-foreground-recipe",cssCustomPropertyName:null}).withDefault({evaluate:(e,t)=>(e=>(t,o)=>function(e,t,o,r,a,i,l){const s=e.source,n=e.closestIndexOf(s),c=d(t)?-1:1,h=n+(1===c?Math.min(r,a):Math.max(c*r,c*a)),u=e.colorContrast(t,o,h,c),p=e.closestIndexOf(u),g=p+c*Math.abs(r-a);let b,m;return(1===c?r<a:c*r>c*a)?(b=p,m=g):(b=g,m=p),{rest:e.get(b),hover:e.get(m),active:e.get(b+c*i),focus:e.get(b+c*l)}}(to.getValueFor(t),o||qe.getValueFor(t),e,ie.getValueFor(t),le.getValueFor(t),se.getValueFor(t),ne.getValueFor(t)))(Xe.normal)(e,t)}),xo=w("error-foreground-rest").withDefault(e=>$o.getValueFor(e).evaluate(e).rest),yo=w("error-foreground-hover").withDefault(e=>$o.getValueFor(e).evaluate(e).hover),ko=w("error-foreground-active").withDefault(e=>$o.getValueFor(e).evaluate(e).active),wo=w("error-foreground-focus").withDefault(e=>$o.getValueFor(e).evaluate(e).focus),Co="--jp-layout-color1";let So=!1;function Fo(){So||(So=!0,function(){const e=()=>{new MutationObserver(()=>{To()}).observe(document.body,{attributes:!0,attributeFilter:["data-jp-theme-name"],childList:!1,characterData:!1}),To()};"complete"===document.readyState?e():window.addEventListener("load",e)}())}const Do=e=>{const t=parseInt(e,10);return isNaN(t)?null:t},Vo={"--jp-border-width":{converter:Do,token:O},"--jp-border-radius":{converter:Do,token:T},[Co]:{converter:(e,t)=>{const o=(0,r.parseColor)(e);if(o){const e=(0,r.rgbToHSL)(o),t=r.ColorHSL.fromObject({h:e.h,s:e.s,l:.5}),a=(0,r.hslToRGB)(t);return i.create(a.r,a.g,a.b)}return null},token:Be},"--jp-brand-color1":{converter:(e,t)=>{const o=(0,r.parseColor)(e);if(o){const e=(0,r.rgbToHSL)(o),a=t?1:-1,l=r.ColorHSL.fromObject({h:e.h,s:e.s,l:e.l+a*oe.getValueFor(document.body)/94}),s=(0,r.hslToRGB)(l);return i.create(s.r,s.g,s.b)}return null},token:je},"--jp-error-color1":{converter:(e,t)=>{const o=(0,r.parseColor)(e);if(o){const e=(0,r.rgbToHSL)(o),a=t?1:-1,l=r.ColorHSL.fromObject({h:e.h,s:e.s,l:e.l+a*oe.getValueFor(document.body)/94}),s=(0,r.hslToRGB)(l);return i.create(s.r,s.g,s.b)}return null},token:eo},"--jp-ui-font-family":{token:S},"--jp-ui-font-size1":{token:I}};function To(){var e;const t=getComputedStyle(document.body),o=document.body.getAttribute("data-jp-theme-light");let a=!1;if(o)a="false"===o;else{const e=t.getPropertyValue(Co).toString();if(e){const t=(0,r.parseColor)(e);t&&(a=d(i.create(t.r,t.g,t.b)),console.debug(`Theme is ${a?"dark":"light"} based on '${Co}' value: ${e}.`))}}V.setValueFor(document.body,a?n.DarkMode:n.LightMode);for(const o in Vo){const r=Vo[o],i=t.getPropertyValue(o).toString();if(document.body&&""!==i){const t=(null!==(e=r.converter)&&void 0!==e?e:e=>e)(i.trim(),a);null!==t?r.token.setValueFor(document.body,t):console.error(`Fail to parse value '${i}' for '${o}' as FAST design token.`)}}}var zo=o(22913);const Bo=(e,t)=>zo.css`
  ${(0,h.display)("flex")} :host {
    box-sizing: border-box;
    flex-direction: column;
    font-family: ${S};
    font-size: ${A};
    line-height: ${P};
    color: ${Wt};
    border-top: calc(${O} * 1px) solid ${Jt};
  }
`,Ho=zo.cssPartial`(${F} + ${z} + ${H}) * ${B}`,jo=(e,t)=>zo.css`
    ${(0,h.display)("flex")} :host {
      box-sizing: border-box;
      font-family: ${S};
      flex-direction: column;
      font-size: ${A};
      line-height: ${P};
      border-bottom: calc(${O} * 1px) solid
        ${Jt};
    }

    .region {
      display: none;
      padding: calc((6 + (${B} * 2 * ${z})) * 1px);
    }

    div.heading {
      display: grid;
      position: relative;
      grid-template-columns: calc(${Ho} * 1px) auto 1fr auto;
      color: ${Wt};
    }

    .button {
      appearance: none;
      border: none;
      background: none;
      grid-column: 3;
      outline: none;
      padding: 0 calc((6 + (${B} * 2 * ${z})) * 1px);
      text-align: left;
      height: calc(${Ho} * 1px);
      color: currentcolor;
      cursor: pointer;
      font-family: inherit;
    }

    .button:hover {
      color: currentcolor;
    }

    .button:active {
      color: currentcolor;
    }

    .button::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      cursor: pointer;
    }

    /* prettier-ignore */
    .button:${h.focusVisible}::before {
      outline: none;
      border: calc(${R} * 1px) solid ${Qe};
      border-radius: calc(${T} * 1px);
    }

    :host([expanded]) .region {
      display: block;
    }

    .icon {
      display: flex;
      align-items: center;
      justify-content: center;
      grid-column: 1;
      grid-row: 1;
      pointer-events: none;
      position: relative;
    }

    slot[name='expanded-icon'],
    slot[name='collapsed-icon'] {
      fill: currentcolor;
    }

    slot[name='collapsed-icon'] {
      display: flex;
    }

    :host([expanded]) slot[name='collapsed-icon'] {
      display: none;
    }

    slot[name='expanded-icon'] {
      display: none;
    }

    :host([expanded]) slot[name='expanded-icon'] {
      display: flex;
    }

    .start {
      display: flex;
      align-items: center;
      padding-inline-start: calc(${B} * 1px);
      justify-content: center;
      grid-column: 2;
      position: relative;
    }

    .end {
      display: flex;
      align-items: center;
      justify-content: center;
      grid-column: 4;
      position: relative;
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      /* prettier-ignore */
      .button:${h.focusVisible}::before {
          border-color: ${u.SystemColors.Highlight};
        }
      :host slot[name='collapsed-icon'],
      :host([expanded]) slot[name='expanded-icon'] {
        fill: ${u.SystemColors.ButtonText};
      }
    `));class Lo extends h.AccordionItem{}const Oo=Lo.compose({baseName:"accordion-item",baseClass:h.AccordionItem,template:h.accordionItemTemplate,styles:jo,collapsedIcon:'\n        <svg\n            width="20"\n            height="20"\n            viewBox="0 0 16 16"\n            xmlns="http://www.w3.org/2000/svg"\n        >\n            <path\n                fill-rule="evenodd"\n                clip-rule="evenodd"\n                d="M5.00001 12.3263C5.00124 12.5147 5.05566 12.699 5.15699 12.8578C5.25831 13.0167 5.40243 13.1437 5.57273 13.2242C5.74304 13.3047 5.9326 13.3354 6.11959 13.3128C6.30659 13.2902 6.4834 13.2152 6.62967 13.0965L10.8988 8.83532C11.0739 8.69473 11.2153 8.51658 11.3124 8.31402C11.4096 8.11146 11.46 7.88966 11.46 7.66499C11.46 7.44033 11.4096 7.21853 11.3124 7.01597C11.2153 6.81341 11.0739 6.63526 10.8988 6.49467L6.62967 2.22347C6.48274 2.10422 6.30501 2.02912 6.11712 2.00691C5.92923 1.9847 5.73889 2.01628 5.56823 2.09799C5.39757 2.17969 5.25358 2.30817 5.153 2.46849C5.05241 2.62882 4.99936 2.8144 5.00001 3.00369V12.3263Z"\n            />\n        </svg>\n    ',expandedIcon:'\n        <svg\n            width="20"\n            height="20"\n            viewBox="0 0 16 16"\n            xmlns="http://www.w3.org/2000/svg"\n        >\n            <path\n                fill-rule="evenodd"\n                clip-rule="evenodd"\n                transform="rotate(90,8,8)"\n          d="M5.00001 12.3263C5.00124 12.5147 5.05566 12.699 5.15699 12.8578C5.25831 13.0167 5.40243 13.1437 5.57273 13.2242C5.74304 13.3047 5.9326 13.3354 6.11959 13.3128C6.30659 13.2902 6.4834 13.2152 6.62967 13.0965L10.8988 8.83532C11.0739 8.69473 11.2153 8.51658 11.3124 8.31402C11.4096 8.11146 11.46 7.88966 11.46 7.66499C11.46 7.44033 11.4096 7.21853 11.3124 7.01597C11.2153 6.81341 11.0739 6.63526 10.8988 6.49467L6.62967 2.22347C6.48274 2.10422 6.30501 2.02912 6.11712 2.00691C5.92923 1.9847 5.73889 2.01628 5.56823 2.09799C5.39757 2.17969 5.25358 2.30817 5.153 2.46849C5.05241 2.62882 4.99936 2.8144 5.00001 3.00369V12.3263Z"\n            />\n        </svg>\n    '});class Ro extends h.Accordion{}const Io=Ro.compose({baseName:"accordion",baseClass:h.Accordion,template:h.accordionTemplate,styles:Bo});function No(e,t,o,r){var a,i=arguments.length,l=i<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,o):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)l=Reflect.decorate(e,t,o,r);else for(var s=e.length-1;s>=0;s--)(a=e[s])&&(l=(i<3?a(l):i>3?a(t,o,l):a(t,o))||l);return i>3&&l&&Object.defineProperty(t,o,l),l}Object.create,Object.create,"function"==typeof SuppressedError&&SuppressedError;const Ao=zo.css`
  ${(0,h.display)("inline-flex")} :host {
    font-family: ${S};
    outline: none;
    font-size: ${I};
    line-height: ${N};
    height: calc(${Ho} * 1px);
    min-width: calc(${Ho} * 1px);
    background-color: ${ft};
    color: ${Wt};
    border-radius: calc(${T} * 1px);
    fill: currentcolor;
    cursor: pointer;
    margin: calc((${R} + 2) * 1px);
  }

  .control {
    background: transparent;
    height: inherit;
    flex-grow: 1;
    box-sizing: border-box;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    padding: 0
      max(
        1px,
        calc((10 + (${B} * 2 * (${z} + ${H})))) * 1px
      );
    white-space: nowrap;
    outline: none;
    text-decoration: none;
    border: calc(${O} * 1px) solid transparent;
    color: inherit;
    border-radius: inherit;
    fill: inherit;
    cursor: inherit;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
  }

  :host(:hover) {
    background-color: ${vt};
  }

  :host(:active) {
    background-color: ${$t};
  }

  :host([aria-pressed='true']) {
    box-shadow: inset 0px 0px 2px 2px ${Lt};
  }

  :host([minimal]),
  :host([scale='xsmall']) {
    --element-scale: -4;
  }

  :host([scale='small']) {
    --element-scale: -2;
  }

  :host([scale='medium']) {
    --element-scale: 0;
  }

  :host([scale='large']) {
    --element-scale: 2;
  }

  :host([scale='xlarge']) {
    --element-scale: 4;
  }

  /* prettier-ignore */
  .control:${h.focusVisible} {
      outline: calc(${R} * 1px) solid ${Ot};
      outline-offset: 2px;
      -moz-outline-radius: 0px;
    }

  .control::-moz-focus-inner {
    border: 0;
  }

  .start,
  .end {
    display: flex;
  }

  .control.icon-only {
    padding: 0;
    line-height: 0;
  }

  ::slotted(svg) {
    ${""} width: 16px;
    height: 16px;
    pointer-events: none;
  }

  .start {
    margin-inline-end: 11px;
  }

  .end {
    margin-inline-start: 11px;
  }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
    :host .control {
      background-color: ${u.SystemColors.ButtonFace};
      border-color: ${u.SystemColors.ButtonText};
      color: ${u.SystemColors.ButtonText};
      fill: currentColor;
    }

    :host(:hover) .control {
      forced-color-adjust: none;
      background-color: ${u.SystemColors.Highlight};
      color: ${u.SystemColors.HighlightText};
    }

    /* prettier-ignore */
    .control:${h.focusVisible} {
          forced-color-adjust: none;
          background-color: ${u.SystemColors.Highlight};
          outline-color: ${u.SystemColors.ButtonText};
          color: ${u.SystemColors.HighlightText};
        }

    .control:hover,
    :host([appearance='outline']) .control:hover {
      border-color: ${u.SystemColors.ButtonText};
    }

    :host([href]) .control {
      border-color: ${u.SystemColors.LinkText};
      color: ${u.SystemColors.LinkText};
    }

    :host([href]) .control:hover,
        :host([href]) .control:${h.focusVisible} {
      forced-color-adjust: none;
      background: ${u.SystemColors.ButtonFace};
      outline-color: ${u.SystemColors.LinkText};
      color: ${u.SystemColors.LinkText};
      fill: currentColor;
    }
  `)),Po=zo.css`
  :host([appearance='accent']) {
    background: ${Ye};
    color: ${ot};
  }

  :host([appearance='accent']:hover) {
    background: ${Ze};
    color: ${rt};
  }

  :host([appearance='accent'][aria-pressed='true']) {
    box-shadow: inset 0px 0px 2px 2px ${gt};
  }

  :host([appearance='accent']:active) .control:active {
    background: ${Je};
    color: ${at};
  }

  :host([appearance="accent"]) .control:${h.focusVisible} {
    outline-color: ${Qe};
  }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
    :host([appearance='accent']) .control {
      forced-color-adjust: none;
      background: ${u.SystemColors.Highlight};
      color: ${u.SystemColors.HighlightText};
    }

    :host([appearance='accent']) .control:hover,
    :host([appearance='accent']:active) .control:active {
      background: ${u.SystemColors.HighlightText};
      border-color: ${u.SystemColors.Highlight};
      color: ${u.SystemColors.Highlight};
    }

    :host([appearance="accent"]) .control:${h.focusVisible} {
      outline-color: ${u.SystemColors.Highlight};
    }

    :host([appearance='accent'][href]) .control {
      background: ${u.SystemColors.LinkText};
      color: ${u.SystemColors.HighlightText};
    }

    :host([appearance='accent'][href]) .control:hover {
      background: ${u.SystemColors.ButtonFace};
      border-color: ${u.SystemColors.LinkText};
      box-shadow: none;
      color: ${u.SystemColors.LinkText};
      fill: currentColor;
    }

    :host([appearance="accent"][href]) .control:${h.focusVisible} {
      outline-color: ${u.SystemColors.HighlightText};
    }
  `)),Eo=zo.css`
  :host([appearance='error']) {
    background: ${ro};
    color: ${ot};
  }

  :host([appearance='error']:hover) {
    background: ${ao};
    color: ${rt};
  }

  :host([appearance='error'][aria-pressed='true']) {
    box-shadow: inset 0px 0px 2px 2px ${ko};
  }

  :host([appearance='error']:active) .control:active {
    background: ${io};
    color: ${at};
  }

  :host([appearance="error"]) .control:${h.focusVisible} {
    outline-color: ${lo};
  }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
    :host([appearance='error']) .control {
      forced-color-adjust: none;
      background: ${u.SystemColors.Highlight};
      color: ${u.SystemColors.HighlightText};
    }

    :host([appearance='error']) .control:hover,
    :host([appearance='error']:active) .control:active {
      background: ${u.SystemColors.HighlightText};
      border-color: ${u.SystemColors.Highlight};
      color: ${u.SystemColors.Highlight};
    }

    :host([appearance="error"]) .control:${h.focusVisible} {
      outline-color: ${u.SystemColors.Highlight};
    }

    :host([appearance='error'][href]) .control {
      background: ${u.SystemColors.LinkText};
      color: ${u.SystemColors.HighlightText};
    }

    :host([appearance='error'][href]) .control:hover {
      background: ${u.SystemColors.ButtonFace};
      border-color: ${u.SystemColors.LinkText};
      box-shadow: none;
      color: ${u.SystemColors.LinkText};
      fill: currentColor;
    }

    :host([appearance="error"][href]) .control:${h.focusVisible} {
      outline-color: ${u.SystemColors.HighlightText};
    }
  `)),Mo=zo.css`
  :host([appearance='hypertext']) {
    font-size: inherit;
    line-height: inherit;
    height: auto;
    min-width: 0;
    background: transparent;
  }

  :host([appearance='hypertext']) .control {
    display: inline;
    padding: 0;
    border: none;
    box-shadow: none;
    border-radius: 0;
    line-height: 1;
  }

  :host a.control:not(:link) {
    background-color: transparent;
    cursor: default;
  }
  :host([appearance='hypertext']) .control:link,
  :host([appearance='hypertext']) .control:visited {
    background: transparent;
    color: ${ut};
    border-bottom: calc(${O} * 1px) solid ${ut};
  }

  :host([appearance='hypertext']:hover),
  :host([appearance='hypertext']) .control:hover {
    background: transparent;
    border-bottom-color: ${pt};
  }

  :host([appearance='hypertext']:active),
  :host([appearance='hypertext']) .control:active {
    background: transparent;
    border-bottom-color: ${gt};
  }

  :host([appearance="hypertext"]) .control:${h.focusVisible} {
    outline-color: transparent;
    border-bottom: calc(${R} * 1px) solid ${At};
    margin-bottom: calc(calc(${O} - ${R}) * 1px);
  }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
    :host([appearance='hypertext']:hover) {
      background-color: ${u.SystemColors.ButtonFace};
      color: ${u.SystemColors.ButtonText};
    }
    :host([appearance="hypertext"][href]) .control:hover,
        :host([appearance="hypertext"][href]) .control:active,
        :host([appearance="hypertext"][href]) .control:${h.focusVisible} {
      color: ${u.SystemColors.LinkText};
      border-bottom-color: ${u.SystemColors.LinkText};
      box-shadow: none;
    }
  `)),Go=zo.css`
  :host([appearance='lightweight']) {
    background: transparent;
    color: ${ut};
  }

  :host([appearance='lightweight']) .control {
    padding: 0;
    height: initial;
    border: none;
    box-shadow: none;
    border-radius: 0;
  }

  :host([appearance='lightweight']:hover) {
    background: transparent;
    color: ${pt};
  }

  :host([appearance='lightweight']:active) {
    background: transparent;
    color: ${gt};
  }

  :host([appearance='lightweight']) .content {
    position: relative;
  }

  :host([appearance='lightweight']) .content::before {
    content: '';
    display: block;
    height: calc(${O} * 1px);
    position: absolute;
    top: calc(1em + 4px);
    width: 100%;
  }

  :host([appearance='lightweight']:hover) .content::before {
    background: ${pt};
  }

  :host([appearance='lightweight']:active) .content::before {
    background: ${gt};
  }

  :host([appearance="lightweight"]) .control:${h.focusVisible} {
    outline-color: transparent;
  }

  :host([appearance="lightweight"]) .control:${h.focusVisible} .content::before {
    background: ${Wt};
    height: calc(${R} * 1px);
  }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
    :host([appearance="lightweight"]) .control:hover,
        :host([appearance="lightweight"]) .control:${h.focusVisible} {
      forced-color-adjust: none;
      background: ${u.SystemColors.ButtonFace};
      color: ${u.SystemColors.Highlight};
    }
    :host([appearance="lightweight"]) .control:hover .content::before,
        :host([appearance="lightweight"]) .control:${h.focusVisible} .content::before {
      background: ${u.SystemColors.Highlight};
    }

    :host([appearance="lightweight"][href]) .control:hover,
        :host([appearance="lightweight"][href]) .control:${h.focusVisible} {
      background: ${u.SystemColors.ButtonFace};
      box-shadow: none;
      color: ${u.SystemColors.LinkText};
    }

    :host([appearance="lightweight"][href]) .control:hover .content::before,
        :host([appearance="lightweight"][href]) .control:${h.focusVisible} .content::before {
      background: ${u.SystemColors.LinkText};
    }
  `)),_o=zo.css`
  :host([appearance='outline']) {
    background: transparent;
    border-color: ${Ye};
  }

  :host([appearance='outline']:hover) {
    border-color: ${Ze};
  }

  :host([appearance='outline']:active) {
    border-color: ${Je};
  }

  :host([appearance='outline']) .control {
    border-color: inherit;
  }

  :host([appearance="outline"]) .control:${h.focusVisible} {
    outline-color: ${Qe};
  }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
    :host([appearance='outline']) .control {
      border-color: ${u.SystemColors.ButtonText};
    }
    :host([appearance="outline"]) .control:${h.focusVisible} {
      forced-color-adjust: none;
      background-color: ${u.SystemColors.Highlight};
      outline-color: ${u.SystemColors.ButtonText};
      color: ${u.SystemColors.HighlightText};
      fill: currentColor;
    }
    :host([appearance='outline'][href]) .control {
      background: ${u.SystemColors.ButtonFace};
      border-color: ${u.SystemColors.LinkText};
      color: ${u.SystemColors.LinkText};
      fill: currentColor;
    }
    :host([appearance="outline"][href]) .control:hover,
        :host([appearance="outline"][href]) .control:${h.focusVisible} {
      forced-color-adjust: none;
      outline-color: ${u.SystemColors.LinkText};
    }
  `)),Wo=zo.css`
  :host([appearance='stealth']),
  :host([appearance='stealth'][disabled]:active),
  :host([appearance='stealth'][disabled]:hover) {
    background: transparent;
  }

  :host([appearance='stealth']:hover) {
    background: ${Vt};
  }

  :host([appearance='stealth']:active) {
    background: ${Tt};
  }

  :host([appearance='stealth']) .control:${h.focusVisible} {
    outline-color: ${Qe};
  }

  /* Make the focus outline displayed within the button if
     it is in a start or end slot; e.g. in a tree item
     This will make the focus outline bounded within the container.
   */
  :host([appearance='stealth'][slot="end"]) .control:${h.focusVisible},
  :host([appearance='stealth'][slot="start"]) .control:${h.focusVisible} {
    outline-offset: -2px;
  }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
    :host([appearance='stealth']),
    :host([appearance='stealth']) .control {
      forced-color-adjust: none;
      background: ${u.SystemColors.ButtonFace};
      border-color: transparent;
      color: ${u.SystemColors.ButtonText};
      fill: currentColor;
    }

    :host([appearance='stealth']:hover) .control {
      background: ${u.SystemColors.Highlight};
      border-color: ${u.SystemColors.Highlight};
      color: ${u.SystemColors.HighlightText};
      fill: currentColor;
    }

    :host([appearance="stealth"]:${h.focusVisible}) .control {
      outline-color: ${u.SystemColors.Highlight};
      color: ${u.SystemColors.HighlightText};
      fill: currentColor;
    }

    :host([appearance='stealth'][href]) .control {
      color: ${u.SystemColors.LinkText};
    }

    :host([appearance="stealth"][href]:hover) .control,
        :host([appearance="stealth"][href]:${h.focusVisible}) .control {
      background: ${u.SystemColors.LinkText};
      border-color: ${u.SystemColors.LinkText};
      color: ${u.SystemColors.HighlightText};
      fill: currentColor;
    }

    :host([appearance="stealth"][href]:${h.focusVisible}) .control {
      forced-color-adjust: none;
      box-shadow: 0 0 0 1px ${u.SystemColors.LinkText};
    }
  `));function Uo(e,t){return new h.PropertyStyleSheetBehavior("appearance",e,t)}const qo=(e,t)=>zo.css`
    ${Ao}
  `.withBehaviors(Uo("accent",Po),Uo("hypertext",Mo),Uo("lightweight",Go),Uo("outline",_o),Uo("stealth",Wo));class Xo extends h.Anchor{appearanceChanged(e,t){this.$fastController.isConnected&&(this.classList.remove(e),this.classList.add(t))}connectedCallback(){super.connectedCallback(),this.appearance||(this.appearance="neutral")}defaultSlottedContentChanged(e,t){const o=this.defaultSlottedContent.filter(e=>e.nodeType===Node.ELEMENT_NODE);1===o.length&&o[0]instanceof SVGElement?this.control.classList.add("icon-only"):this.control.classList.remove("icon-only")}}No([zo.attr],Xo.prototype,"appearance",void 0);const Ko=Xo.compose({baseName:"anchor",baseClass:h.Anchor,template:h.anchorTemplate,styles:qo,shadowOptions:{delegatesFocus:!0}}),Yo=(e,t)=>zo.css`
  :host {
    contain: layout;
    display: block;
  }
`;class Zo extends h.AnchoredRegion{}const Jo=Zo.compose({baseName:"anchored-region",baseClass:h.AnchoredRegion,template:h.anchoredRegionTemplate,styles:Yo});class Qo{constructor(e,t){this.cache=new WeakMap,this.ltr=e,this.rtl=t}bind(e){this.attach(e)}unbind(e){const t=this.cache.get(e);t&&j.unsubscribe(t)}attach(e){const t=this.cache.get(e)||new er(this.ltr,this.rtl,e),o=j.getValueFor(e);j.subscribe(t),t.attach(o),this.cache.set(e,t)}}class er{constructor(e,t,o){this.ltr=e,this.rtl=t,this.source=o,this.attached=null}handleChange({target:e,token:t}){this.attach(t.getValueFor(e))}attach(e){this.attached!==this[e]&&(null!==this.attached&&this.source.$fastController.removeStyles(this.attached),this.attached=this[e],null!==this.attached&&this.source.$fastController.addStyles(this.attached))}}const tr=(e,t)=>zo.css`
    ${(0,h.display)("flex")} :host {
      position: relative;
      height: var(--avatar-size, var(--avatar-size-default));
      width: var(--avatar-size, var(--avatar-size-default));
      --avatar-size-default: calc(
        (
            (${F} + ${z}) * ${B} +
              ((${B} * 8) - 40)
          ) * 1px
      );
      --avatar-text-size: ${I};
      --avatar-text-ratio: ${B};
    }

    .link {
      text-decoration: none;
      color: ${Wt};
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      min-width: 100%;
    }

    .square {
      border-radius: calc(${T} * 1px);
      min-width: 100%;
      overflow: hidden;
    }

    .circle {
      border-radius: 100%;
      min-width: 100%;
      overflow: hidden;
    }

    .backplate {
      position: relative;
      display: flex;
      background-color: ${Ye};
    }

    .media,
    ::slotted(img) {
      max-width: 100%;
      position: absolute;
      display: block;
    }

    .content {
      font-size: calc(
        (
            var(--avatar-text-size) +
              var(--avatar-size, var(--avatar-size-default))
          ) / var(--avatar-text-ratio)
      );
      line-height: var(--avatar-size, var(--avatar-size-default));
      display: block;
      min-height: var(--avatar-size, var(--avatar-size-default));
    }

    ::slotted(${e.tagFor(h.Badge)}) {
      position: absolute;
      display: block;
    }
  `.withBehaviors(new Qo((e=>zo.css`
  ::slotted(${e.tagFor(h.Badge)}) {
    right: 0;
  }
`)(e),(e=>zo.css`
  ::slotted(${e.tagFor(h.Badge)}) {
    left: 0;
  }
`)(e)));class or extends h.Avatar{}No([(0,zo.attr)({attribute:"src"})],or.prototype,"imgSrc",void 0),No([zo.attr],or.prototype,"alt",void 0);const rr=zo.html`
  ${(0,zo.when)(e=>e.imgSrc,zo.html`
      <img
        src="${e=>e.imgSrc}"
        alt="${e=>e.alt}"
        slot="media"
        class="media"
        part="media"
      />
    `)}
`,ar=or.compose({baseName:"avatar",baseClass:h.Avatar,template:h.avatarTemplate,styles:tr,media:rr,shadowOptions:{delegatesFocus:!0}}),ir=(e,t)=>zo.css`
  ${(0,h.display)("inline-block")} :host {
    box-sizing: border-box;
    font-family: ${S};
    font-size: ${A};
    line-height: ${P};
  }

  .control {
    border-radius: calc(${T} * 1px);
    padding: calc(((${B} * 0.5) - ${O}) * 1px)
      calc((${B} - ${O}) * 1px);
    color: ${Wt};
    font-weight: 600;
    border: calc(${O} * 1px) solid transparent;
    background-color: ${ft};
  }

  .control[style] {
    font-weight: 400;
  }

  :host([circular]) .control {
    border-radius: 100px;
    padding: 0 calc(${B} * 1px);
    height: calc((${Ho} - (${B} * 3)) * 1px);
    min-width: calc((${Ho} - (${B} * 3)) * 1px);
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
  }
`;class lr extends h.Badge{}const sr=lr.compose({baseName:"badge",baseClass:h.Badge,template:h.badgeTemplate,styles:ir}),nr=(e,t)=>zo.css`
  ${(0,h.display)("inline-block")} :host {
    box-sizing: border-box;
    font-family: ${S};
    font-size: ${I};
    line-height: ${N};
  }

  .list {
    display: flex;
    flex-wrap: wrap;
  }
`;class cr extends h.Breadcrumb{}const dr=cr.compose({baseName:"breadcrumb",baseClass:h.Breadcrumb,template:h.breadcrumbTemplate,styles:nr}),hr=(e,t)=>zo.css`
    ${(0,h.display)("inline-flex")} :host {
        background: transparent;
        box-sizing: border-box;
        font-family: ${S};
        font-size: ${I};
        fill: currentColor;
        line-height: ${N};
        min-width: calc(${Ho} * 1px);
        outline: none;
        color: ${Wt}
    }

    .listitem {
        display: flex;
        align-items: center;
        width: max-content;
    }

    .separator {
        margin: 0 6px;
        display: flex;
    }

    .control {
        align-items: center;
        box-sizing: border-box;
        color: ${ut};
        cursor: pointer;
        display: flex;
        fill: inherit;
        outline: none;
        text-decoration: none;
        white-space: nowrap;
    }

    .control:hover {
        color: ${pt};
    }

    .control:active {
        color: ${gt};
    }

    .control .content {
        position: relative;
    }

    .control .content::before {
        content: "";
        display: block;
        height: calc(${O} * 1px);
        left: 0;
        position: absolute;
        right: 0;
        top: calc(1em + 4px);
        width: 100%;
    }

    .control:hover .content::before {
        background: ${pt};
    }

    .control:active .content::before {
        background: ${gt};
    }

    .control:${h.focusVisible} .content::before {
        background: ${bt};
        height: calc(${R} * 1px);
    }

    .control:not([href]) {
        color: ${Wt};
        cursor: default;
    }

    .control:not([href]) .content::before {
        background: none;
    }

    .start,
    .end {
        display: flex;
    }

    ::slotted(svg) {
        /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
        width: 16px;
        height: 16px;
    }

    .start {
        margin-inline-end: 6px;
    }

    .end {
        margin-inline-start: 6px;
    }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      .control:hover .content::before,
                .control:${h.focusVisible} .content::before {
        background: ${u.SystemColors.LinkText};
      }
      .start,
      .end {
        fill: ${u.SystemColors.ButtonText};
      }
    `));class ur extends h.BreadcrumbItem{}const pr=ur.compose({baseName:"breadcrumb-item",baseClass:h.BreadcrumbItem,template:h.breadcrumbItemTemplate,styles:hr,separator:"/",shadowOptions:{delegatesFocus:!0}}),gr=(e,t)=>zo.css`
    :host([disabled]),
    :host([disabled]:hover),
    :host([disabled]:active) {
      opacity: ${L};
      background-color: ${ft};
      cursor: ${h.disabledCursor};
    }

    ${Ao}
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host([disabled]),
      :host([disabled]) .control,
      :host([disabled]:hover),
      :host([disabled]:active) {
        forced-color-adjust: none;
        background-color: ${u.SystemColors.ButtonFace};
        outline-color: ${u.SystemColors.GrayText};
        color: ${u.SystemColors.GrayText};
        cursor: ${h.disabledCursor};
        opacity: 1;
      }
    `),Uo("accent",zo.css`
        :host([appearance='accent'][disabled]),
        :host([appearance='accent'][disabled]:hover),
        :host([appearance='accent'][disabled]:active) {
          background: ${Ye};
        }

        ${Po}
      `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
          :host([appearance='accent'][disabled]) .control,
          :host([appearance='accent'][disabled]) .control:hover {
            background: ${u.SystemColors.ButtonFace};
            border-color: ${u.SystemColors.GrayText};
            color: ${u.SystemColors.GrayText};
          }
        `))),Uo("error",zo.css`
        :host([appearance='error'][disabled]),
        :host([appearance='error'][disabled]:hover),
        :host([appearance='error'][disabled]:active) {
          background: ${ro};
        }

        ${Eo}
      `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
          :host([appearance='error'][disabled]) .control,
          :host([appearance='error'][disabled]) .control:hover {
            background: ${u.SystemColors.ButtonFace};
            border-color: ${u.SystemColors.GrayText};
            color: ${u.SystemColors.GrayText};
          }
        `))),Uo("lightweight",zo.css`
        :host([appearance='lightweight'][disabled]:hover),
        :host([appearance='lightweight'][disabled]:active) {
          background-color: transparent;
          color: ${ut};
        }

        :host([appearance='lightweight'][disabled]) .content::before,
        :host([appearance='lightweight'][disabled]:hover) .content::before,
        :host([appearance='lightweight'][disabled]:active) .content::before {
          background: transparent;
        }

        ${Go}
      `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
          :host([appearance='lightweight'].disabled) .control {
            forced-color-adjust: none;
            color: ${u.SystemColors.GrayText};
          }

          :host([appearance='lightweight'].disabled)
            .control:hover
            .content::before {
            background: none;
          }
        `))),Uo("outline",zo.css`
        :host([appearance='outline'][disabled]),
        :host([appearance='outline'][disabled]:hover),
        :host([appearance='outline'][disabled]:active) {
          background: transparent;
          border-color: ${Ye};
        }

        ${_o}
      `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
          :host([appearance='outline'][disabled]) .control {
            border-color: ${u.SystemColors.GrayText};
          }
        `))),Uo("stealth",zo.css`
        ${Wo}
      `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
          :host([appearance='stealth'][disabled]) {
            background: ${u.SystemColors.ButtonFace};
          }

          :host([appearance='stealth'][disabled]) .control {
            background: ${u.SystemColors.ButtonFace};
            border-color: transparent;
            color: ${u.SystemColors.GrayText};
          }
        `))));class br extends h.Button{constructor(){super(...arguments),this.appearance="neutral"}defaultSlottedContentChanged(e,t){const o=this.defaultSlottedContent.filter(e=>e.nodeType===Node.ELEMENT_NODE);1===o.length&&(o[0]instanceof SVGElement||o[0].classList.contains("fa")||o[0].classList.contains("fas"))?this.control.classList.add("icon-only"):this.control.classList.remove("icon-only")}}No([zo.attr],br.prototype,"appearance",void 0),No([(0,zo.attr)({attribute:"minimal",mode:"boolean"})],br.prototype,"minimal",void 0),No([zo.attr],br.prototype,"scale",void 0);const mr=br.compose({baseName:"button",baseClass:h.Button,template:h.buttonTemplate,styles:gr,shadowOptions:{delegatesFocus:!0}}),fr="box-shadow: 0 0 calc((var(--elevation) * 0.225px) + 2px) rgba(0, 0, 0, calc(.11 * (2 - var(--background-luminance, 1)))), 0 calc(var(--elevation) * 0.4px) calc((var(--elevation) * 0.9px)) rgba(0, 0, 0, calc(.13 * (2 - var(--background-luminance, 1))));",vr=(e,t)=>zo.css`
    ${(0,h.display)("block")} :host {
      --elevation: 4;
      display: block;
      contain: content;
      height: var(--card-height, 100%);
      width: var(--card-width, 100%);
      box-sizing: border-box;
      background: ${qe};
      border-radius: calc(${T} * 1px);
      ${fr}
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        forced-color-adjust: none;
        background: ${u.SystemColors.Canvas};
        box-shadow: 0 0 0 1px ${u.SystemColors.CanvasText};
      }
    `));class $r extends h.Card{connectedCallback(){super.connectedCallback();const e=(0,h.composedParent)(this);e&&qe.setValueFor(this,t=>Rt.getValueFor(t).evaluate(t,qe.getValueFor(e)))}}const xr=$r.compose({baseName:"card",baseClass:h.Card,template:h.cardTemplate,styles:vr}),yr=(e,t)=>zo.css`
    ${(0,h.display)("inline-flex")} :host {
      align-items: center;
      outline: none;
      margin: calc(${B} * 1px) 0;
      /* Chromium likes to select label text or the default slot when the checkbox is
            clicked. Maybe there is a better solution here? */
      user-select: none;
    }

    .control {
      position: relative;
      width: calc((${Ho} / 2 + ${B}) * 1px);
      height: calc((${Ho} / 2 + ${B}) * 1px);
      box-sizing: border-box;
      border-radius: calc(${T} * 1px);
      border: calc(${O} * 1px) solid ${qt};
      background: ${kt};
      outline: none;
      cursor: pointer;
    }

    :host([aria-invalid='true']) .control {
      border-color: ${ro};
    }

    .label {
      font-family: ${S};
      color: ${Wt};
      /* Need to discuss with Brian how HorizontalSpacingNumber can work.
            https://github.com/microsoft/fast/issues/2766 */
      padding-inline-start: calc(${B} * 2px + 2px);
      margin-inline-end: calc(${B} * 2px + 2px);
      cursor: pointer;
      font-size: ${I};
      line-height: ${N};
    }

    .label__hidden {
      display: none;
      visibility: hidden;
    }

    .checked-indicator {
      width: 100%;
      height: 100%;
      display: block;
      fill: ${ot};
      opacity: 0;
      pointer-events: none;
    }

    .indeterminate-indicator {
      border-radius: calc(${T} * 1px);
      background: ${ot};
      position: absolute;
      top: 50%;
      left: 50%;
      width: 50%;
      height: 50%;
      transform: translate(-50%, -50%);
      opacity: 0;
    }

    :host(:not([disabled])) .control:hover {
      background: ${wt};
      border-color: ${Xt};
    }

    :host(:not([disabled])) .control:active {
      background: ${Ct};
      border-color: ${Kt};
    }

    :host([aria-invalid='true']:not([disabled])) .control:hover {
      border-color: ${ao};
    }

    :host([aria-invalid='true']:not([disabled])) .control:active {
      border-color: ${io};
    }

    :host(:${h.focusVisible}) .control {
      outline: calc(${R} * 1px) solid ${Qe};
      outline-offset: 2px;
    }

    :host([aria-invalid='true']:${h.focusVisible}) .control {
      outline-color: ${lo};
    }

    :host([aria-checked='true']) .control {
      background: ${Ye};
      border: calc(${O} * 1px) solid ${Ye};
    }

    :host([aria-checked='true']:not([disabled])) .control:hover {
      background: ${Ze};
      border: calc(${O} * 1px) solid ${Ze};
    }

    :host([aria-invalid='true'][aria-checked='true']) .control {
      background-color: ${ro};
      border-color: ${ro};
    }

    :host([aria-invalid='true'][aria-checked='true']:not([disabled]))
      .control:hover {
      background-color: ${ao};
      border-color: ${ao};
    }

    :host([aria-checked='true']:not([disabled]))
      .control:hover
      .checked-indicator {
      fill: ${rt};
    }

    :host([aria-checked='true']:not([disabled]))
      .control:hover
      .indeterminate-indicator {
      background: ${rt};
    }

    :host([aria-checked='true']:not([disabled])) .control:active {
      background: ${Je};
      border: calc(${O} * 1px) solid ${Je};
    }

    :host([aria-invalid='true'][aria-checked='true']:not([disabled]))
      .control:active {
      background-color: ${io};
      border-color: ${io};
    }

    :host([aria-checked='true']:not([disabled]))
      .control:active
      .checked-indicator {
      fill: ${at};
    }

    :host([aria-checked='true']:not([disabled]))
      .control:active
      .indeterminate-indicator {
      background: ${at};
    }

    :host([aria-checked="true"]:${h.focusVisible}:not([disabled])) .control {
      outline: calc(${R} * 1px) solid ${Qe};
      outline-offset: 2px;
    }

    :host([aria-invalid='true'][aria-checked="true"]:${h.focusVisible}:not([disabled])) .control {
      outline-color: ${lo};
    }

    :host([disabled]) .label,
    :host([readonly]) .label,
    :host([readonly]) .control,
    :host([disabled]) .control {
      cursor: ${h.disabledCursor};
    }

    :host([aria-checked='true']:not(.indeterminate)) .checked-indicator,
    :host(.indeterminate) .indeterminate-indicator {
      opacity: 1;
    }

    :host([disabled]) {
      opacity: ${L};
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      .control {
        forced-color-adjust: none;
        border-color: ${u.SystemColors.FieldText};
        background: ${u.SystemColors.Field};
      }
      :host([aria-invalid='true']) .control {
        border-style: dashed;
      }
      .checked-indicator {
        fill: ${u.SystemColors.FieldText};
      }
      .indeterminate-indicator {
        background: ${u.SystemColors.FieldText};
      }
      :host(:not([disabled])) .control:hover,
      .control:active {
        border-color: ${u.SystemColors.Highlight};
        background: ${u.SystemColors.Field};
      }
      :host(:${h.focusVisible}) .control {
        outline: calc(${R} * 1px) solid ${u.SystemColors.FieldText};
        outline-offset: 2px;
      }
      :host([aria-checked="true"]:${h.focusVisible}:not([disabled])) .control {
        outline: calc(${R} * 1px) solid ${u.SystemColors.FieldText};
        outline-offset: 2px;
      }
      :host([aria-checked='true']) .control {
        background: ${u.SystemColors.Highlight};
        border-color: ${u.SystemColors.Highlight};
      }
      :host([aria-checked='true']:not([disabled])) .control:hover,
      .control:active {
        border-color: ${u.SystemColors.Highlight};
        background: ${u.SystemColors.HighlightText};
      }
      :host([aria-checked='true']) .checked-indicator {
        fill: ${u.SystemColors.HighlightText};
      }
      :host([aria-checked='true']:not([disabled]))
        .control:hover
        .checked-indicator {
        fill: ${u.SystemColors.Highlight};
      }
      :host([aria-checked='true']) .indeterminate-indicator {
        background: ${u.SystemColors.HighlightText};
      }
      :host([aria-checked='true']) .control:hover .indeterminate-indicator {
        background: ${u.SystemColors.Highlight};
      }
      :host([disabled]) {
        opacity: 1;
      }
      :host([disabled]) .control {
        forced-color-adjust: none;
        border-color: ${u.SystemColors.GrayText};
        background: ${u.SystemColors.Field};
      }
      :host([disabled]) .indeterminate-indicator,
      :host([aria-checked='true'][disabled])
        .control:hover
        .indeterminate-indicator {
        forced-color-adjust: none;
        background: ${u.SystemColors.GrayText};
      }
      :host([disabled]) .checked-indicator,
      :host([aria-checked='true'][disabled]) .control:hover .checked-indicator {
        forced-color-adjust: none;
        fill: ${u.SystemColors.GrayText};
      }
    `)),kr=(e,t)=>zo.html`
  <template
    role="checkbox"
    aria-checked="${e=>e.checked}"
    aria-required="${e=>e.required}"
    aria-disabled="${e=>e.disabled}"
    aria-readonly="${e=>e.readOnly}"
    tabindex="${e=>e.disabled?null:0}"
    @keypress="${(e,t)=>e.keypressHandler(t.event)}"
    @click="${(e,t)=>e.clickHandler(t.event)}"
  >
    <div part="control" class="control">
      <slot name="checked-indicator">
        ${t.checkedIndicator||""}
      </slot>
      <slot name="indeterminate-indicator">
        ${t.indeterminateIndicator||""}
      </slot>
    </div>
    <label
      part="label"
      class="${e=>e.defaultSlottedNodes&&e.defaultSlottedNodes.length?"label":"label label__hidden"}"
    >
      <slot ${(0,zo.slotted)("defaultSlottedNodes")}></slot>
    </label>
  </template>
`;class wr extends h.Checkbox{indeterminateChanged(e,t){this.indeterminate?this.classList.add("indeterminate"):this.classList.remove("indeterminate")}}const Cr=wr.compose({baseName:"checkbox",baseClass:h.Checkbox,template:kr,styles:yr,checkedIndicator:'\n        <svg\n            part="checked-indicator"\n            class="checked-indicator"\n            viewBox="0 0 20 20"\n            xmlns="http://www.w3.org/2000/svg"\n        >\n            <path\n                fill-rule="evenodd"\n                clip-rule="evenodd"\n                d="M8.143 12.6697L15.235 4.5L16.8 5.90363L8.23812 15.7667L3.80005 11.2556L5.27591 9.7555L8.143 12.6697Z"\n            />\n        </svg>\n    ',indeterminateIndicator:'\n        <div part="indeterminate-indicator" class="indeterminate-indicator"></div>\n    '}),Sr=(e,t)=>{const o=e.tagFor(h.ListboxOption),r=e.name===e.tagFor(h.ListboxElement)?"":".listbox";return zo.css`
        ${r?"":(0,h.display)("inline-flex")}

        :host ${r} {
            background: ${qe};
            border: calc(${O} * 1px) solid ${qt};
            border-radius: calc(${T} * 1px);
            box-sizing: border-box;
            flex-direction: column;
            padding: calc(${B} * 1px) 0;
        }

        ${r?"":zo.css`
:host(:${h.focusVisible}:not([disabled])) {
                outline: none;
            }

            :host(:focus-within:not([disabled])) {
                border-color: ${At};
                box-shadow: 0 0 0
                    calc((${R} - ${O}) * 1px)
                    ${At} inset;
            }

            :host([disabled]) ::slotted(*) {
                cursor: ${h.disabledCursor};
                opacity: ${L};
                pointer-events: none;
            }
        `}

        ${r||":host([size])"} {
            max-height: calc(
                (var(--size) * ${Ho} + (${B} * ${O} * 2)) * 1px
            );
            overflow-y: auto;
        }

        :host([size="0"]) ${r} {
            max-height: none;
        }
    `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
                :host(:not([multiple]):${h.focusVisible}) ::slotted(${o}[aria-selected="true"]),
                :host([multiple]:${h.focusVisible}) ::slotted(${o}[aria-checked="true"]) {
                    border-color: ${u.SystemColors.ButtonText};
                    box-shadow: 0 0 0 calc(${R} * 1px) inset ${u.SystemColors.HighlightText};
                }

                :host(:not([multiple]):${h.focusVisible}) ::slotted(${o}[aria-selected="true"]) {
                    background: ${u.SystemColors.Highlight};
                    color: ${u.SystemColors.HighlightText};
                    fill: currentcolor;
                }

                ::slotted(${o}[aria-selected="true"]:not([aria-checked="true"])) {
                    background: ${u.SystemColors.Highlight};
                    border-color: ${u.SystemColors.HighlightText};
                    color: ${u.SystemColors.HighlightText};
                }
            `))},Fr=(e,t)=>{const o=e.name===e.tagFor(h.Select);return zo.css`
  ${(0,h.display)("inline-flex")}
  
  :host {
    --elevation: 14;
    background: ${kt};
    border-radius: calc(${T} * 1px);
    border: calc(${O} * 1px) solid ${Ht};
    box-sizing: border-box;
    color: ${Wt};
    font-family: ${S};
    height: calc(${Ho} * 1px);
    position: relative;
    user-select: none;
    min-width: 250px;
    outline: none;
    vertical-align: top;
  }

  :host([aria-invalid='true']) {
    border-color: ${ro};
  }
  
  :host(:not([autowidth])) {
    min-width: 250px;
  }
  
  ${o?zo.css`
  :host(:not([aria-haspopup])) {
    --elevation: 0;
    border: 0;
    height: auto;
    min-width: 0;
  }
  `:""}
  
  ${Sr(e,t)}
  
  :host .listbox {
    ${fr}
    border: none;
    display: flex;
    left: 0;
    position: absolute;
    width: 100%;
    z-index: 1;
  }
  
  .control + .listbox {
    --stroke-size: calc(${B} * ${O} * 2);
    max-height: calc(
      (var(--listbox-max-height) * ${Ho} + var(--stroke-size)) * 1px
      );
  }
  
  ${o?zo.css`
  :host(:not([aria-haspopup])) .listbox {
    left: auto;
    position: static;
    z-index: auto;
  }
  `:""}
  
  :host(:not([autowidth])) .listbox {
    width: 100%;
  }
  
  :host([autowidth]) ::slotted([role='option']),
  :host([autowidth]) ::slotted(option) {
    padding: 0 calc(1em + ${B} * 1.25px + 1px);
  }
  
  .listbox[hidden] {
    display: none;
  }
  
  .control {
    align-items: center;
    box-sizing: border-box;
    cursor: pointer;
    display: flex;
    font-size: ${I};
    font-family: inherit;
    line-height: ${N};
    min-height: 100%;
    padding: 0 calc(${B} * 2.25px);
    width: 100%;
  }

  :host([minimal]),
  :host([scale='xsmall']) {
    --element-scale: -4;
  }

  :host([scale='small']) {
    --element-scale: -2;
  }

  :host([scale='medium']) {
    --element-scale: 0;
  }

  :host([scale='large']) {
    --element-scale: 2;
  }

  :host([scale='xlarge']) {
    --element-scale: 4;
  }
  
  :host(:not([disabled]):hover) {
    background: ${wt};
    border-color: ${jt};
  }
  
  :host([aria-invalid='true']:not([disabled]):hover) {
    border-color: ${ao};
  }
  
  :host(:${h.focusVisible}) {
    border-color: ${Qe};
    box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
    ${Qe};
  }
  
  :host([aria-invalid='true']:${h.focusVisible}) {
    border-color: ${lo};
    box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
    ${lo};
  }
  
  :host(:not([size]):not([multiple]):not([open]):${h.focusVisible}),
  :host([multiple]:${h.focusVisible}),
  :host([size]:${h.focusVisible}) {
    box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
    ${Qe};
  }
  
  :host([aria-invalid='true']:not([size]):not([multiple]):not([open]):${h.focusVisible}),
  :host([aria-invalid='true'][multiple]:${h.focusVisible}),
  :host([aria-invalid='true'][size]:${h.focusVisible}) {
    box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
    ${lo};
  }
  
  :host(:not([multiple]):not([size]):${h.focusVisible}) ::slotted(${e.tagFor(h.ListboxOption)}[aria-selected="true"]:not([disabled])) {
    box-shadow: 0 0 0 calc(${R} * 1px) inset ${Qe};
    border-color: ${Qe};
    background: ${Qe};
    color: ${it};
  }
    
  :host([disabled]) {
    cursor: ${h.disabledCursor};
    opacity: ${L};
  }
  
  :host([disabled]) .control {
    cursor: ${h.disabledCursor};
    user-select: none;
  }
  
  :host([disabled]:hover) {
    background: ${Dt};
    color: ${Wt};
    fill: currentcolor;
  }
  
  :host(:not([disabled])) .control:active {
    background: ${Ct};
    border-color: ${Je};
    border-radius: calc(${T} * 1px);
  }
  
  :host([open][position="above"]) .listbox {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    border-bottom: 0;
    bottom: calc(${Ho} * 1px);
  }
  
  :host([open][position="below"]) .listbox {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    border-top: 0;
    top: calc(${Ho} * 1px);
  }
  
  .selected-value {
    flex: 1 1 auto;
    font-family: inherit;
    overflow: hidden;
    text-align: start;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .indicator {
    flex: 0 0 auto;
    margin-inline-start: 1em;
  }
  
  slot[name="listbox"] {
    display: none;
    width: 100%;
  }
  
  :host([open]) slot[name="listbox"] {
    display: flex;
    position: absolute;
    ${fr}
  }
  
  .end {
    margin-inline-start: auto;
  }
  
  .start,
  .end,
  .indicator,
  .select-indicator,
  ::slotted(svg) {
    /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
    fill: currentcolor;
    height: 1em;
    min-height: calc(${B} * 4px);
    min-width: calc(${B} * 4px);
    width: 1em;
  }
  
  ::slotted([role="option"]),
  ::slotted(option) {
    flex: 0 0 auto;
  }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host(:not([disabled]):hover),
      :host(:not([disabled]):active) {
        border-color: ${u.SystemColors.Highlight};
      }

      :host([aria-invalid='true']) {
        border-style: dashed;
      }
      
      :host(:not([disabled]):${h.focusVisible}) {
        background-color: ${u.SystemColors.ButtonFace};
        box-shadow: 0 0 0 calc(${R} * 1px) ${u.SystemColors.Highlight};
        color: ${u.SystemColors.ButtonText};
        fill: currentcolor;
        forced-color-adjust: none;
      }
      
      :host(:not([disabled]):${h.focusVisible}) .listbox {
        background: ${u.SystemColors.ButtonFace};
      }
      
      :host([disabled]) {
        border-color: ${u.SystemColors.GrayText};
        background-color: ${u.SystemColors.ButtonFace};
        color: ${u.SystemColors.GrayText};
        fill: currentcolor;
        opacity: 1;
        forced-color-adjust: none;
      }
      
      :host([disabled]:hover) {
        background: ${u.SystemColors.ButtonFace};
      }
      
      :host([disabled]) .control {
        color: ${u.SystemColors.GrayText};
        border-color: ${u.SystemColors.GrayText};
      }
      
      :host([disabled]) .control .select-indicator {
        fill: ${u.SystemColors.GrayText};
      }
      
      :host(:${h.focusVisible}) ::slotted([aria-selected="true"][role="option"]),
      :host(:${h.focusVisible}) ::slotted(option[aria-selected="true"]),
      :host(:${h.focusVisible}) ::slotted([aria-selected="true"][role="option"]:not([disabled])) {
        background: ${u.SystemColors.Highlight};
        border-color: ${u.SystemColors.ButtonText};
        box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
        ${u.SystemColors.HighlightText};
        color: ${u.SystemColors.HighlightText};
        fill: currentcolor;
      }
      
      .start,
      .end,
      .indicator,
      .select-indicator,
      ::slotted(svg) {
        color: ${u.SystemColors.ButtonText};
        fill: currentcolor;
      }
      `))},Dr=(e,t)=>zo.css`
  ${Fr(e,t)}

  :host(:empty) .listbox {
    display: none;
  }

  :host([disabled]) *,
  :host([disabled]) {
    cursor: ${h.disabledCursor};
    user-select: none;
  }

  :host(:focus-within:not([disabled])) {
    border-color: ${Qe};
    box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
      ${Qe};
  }

  :host([aria-invalid='true']:focus-within:not([disabled])) {
    border-color: ${lo};
    box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
      ${lo};
  }

  .selected-value {
    -webkit-appearance: none;
    background: transparent;
    border: none;
    color: inherit;
    font-size: ${I};
    line-height: ${N};
    height: calc(100% - (${O} * 1px));
    margin: auto 0;
    width: 100%;
  }

  .selected-value:hover,
    .selected-value:${h.focusVisible},
    .selected-value:disabled,
    .selected-value:active {
    outline: none;
  }
`;class Vr extends h.Combobox{connectedCallback(){super.connectedCallback(),this.setAutoWidth()}slottedOptionsChanged(e,t){super.slottedOptionsChanged(e,t),this.setAutoWidth()}autoWidthChanged(e,t){t?this.setAutoWidth():this.style.removeProperty("width")}setAutoWidth(){if(!this.autoWidth||!this.isConnected)return;let e=this.listbox.getBoundingClientRect().width;0===e&&this.listbox.hidden&&(Object.assign(this.listbox.style,{visibility:"hidden"}),this.listbox.removeAttribute("hidden"),e=this.listbox.getBoundingClientRect().width,this.listbox.setAttribute("hidden",""),this.listbox.style.removeProperty("visibility")),e>0&&Object.assign(this.style,{width:`${e}px`})}maxHeightChanged(e,t){this.updateComputedStylesheet()}updateComputedStylesheet(){this.computedStylesheet&&this.$fastController.removeStyles(this.computedStylesheet);const e=Math.floor(this.maxHeight/Qt.getValueFor(this)).toString();this.computedStylesheet=zo.css`
      :host {
        --listbox-max-height: ${e};
      }
    `,this.$fastController.addStyles(this.computedStylesheet)}}No([(0,zo.attr)({attribute:"autowidth",mode:"boolean"})],Vr.prototype,"autoWidth",void 0),No([(0,zo.attr)({attribute:"minimal",mode:"boolean"})],Vr.prototype,"minimal",void 0),No([zo.attr],Vr.prototype,"scale",void 0);const Tr=Vr.compose({baseName:"combobox",baseClass:h.Combobox,template:h.comboboxTemplate,styles:Dr,shadowOptions:{delegatesFocus:!0},indicator:'\n        <svg\n            class="select-indicator"\n            part="select-indicator"\n            viewBox="0 0 12 7"\n            xmlns="http://www.w3.org/2000/svg"\n        >\n            <path\n                d="M11.85.65c.2.2.2.5 0 .7L6.4 6.84a.55.55 0 01-.78 0L.14 1.35a.5.5 0 11.71-.7L6 5.8 11.15.65c.2-.2.5-.2.7 0z"\n            />\n        </svg>\n    '}),zr=(e,t)=>zo.css`
  :host {
    display: flex;
    position: relative;
    flex-direction: column;
  }
`,Br=(e,t)=>zo.css`
  :host {
    display: grid;
    padding: 1px 0;
    box-sizing: border-box;
    width: 100%;
    border-bottom: calc(${O} * 1px) solid ${Jt};
  }

  :host(.header) {
  }

  :host(.sticky-header) {
    background: ${ft};
    position: sticky;
    top: 0;
  }
`,Hr=(e,t)=>zo.css`
    :host {
      padding: calc(${B} * 1px) calc(${B} * 3px);
      color: ${Wt};
      box-sizing: border-box;
      font-family: ${S};
      font-size: ${I};
      line-height: ${N};
      font-weight: 400;
      border: transparent calc(${R} * 1px) solid;
      overflow: hidden;
      white-space: nowrap;
      border-radius: calc(${T} * 1px);
    }

    :host(.column-header) {
      font-weight: 600;
    }

    :host(:${h.focusVisible}) {
      outline: calc(${R} * 1px) solid ${Qe};
      color: ${Wt};
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        forced-color-adjust: none;
        border-color: transparent;
        background: ${u.SystemColors.Field};
        color: ${u.SystemColors.FieldText};
      }

      :host(:${h.focusVisible}) {
        border-color: ${u.SystemColors.FieldText};
        box-shadow: 0 0 0 2px inset ${u.SystemColors.Field};
        color: ${u.SystemColors.FieldText};
      }
    `));class jr extends h.DataGridCell{}const Lr=jr.compose({baseName:"data-grid-cell",baseClass:h.DataGridCell,template:h.dataGridCellTemplate,styles:Hr});class Or extends h.DataGridRow{}const Rr=Or.compose({baseName:"data-grid-row",baseClass:h.DataGridRow,template:h.dataGridRowTemplate,styles:Br});class Ir extends h.DataGrid{}const Nr=Ir.compose({baseName:"data-grid",baseClass:h.DataGrid,template:h.dataGridTemplate,styles:zr});class Ar extends h.FoundationElement{}class Pr extends((0,h.FormAssociated)(Ar)){constructor(){super(...arguments),this.proxy=document.createElement("input")}}const Er={toView(e){if(null==e)return null;const t=new Date(e);return"Invalid Date"===t.toString()?null:`${t.getFullYear().toString().padStart(4,"0")}-${(t.getMonth()+1).toString().padStart(2,"0")}-${t.getDate().toString().padStart(2,"0")}`},fromView(e){if(null==e)return null;const t=new Date(e);return"Invalid Date"===t.toString()?null:t}},Mr="Invalid Date";class Gr extends Pr{constructor(){super(...arguments),this.step=1,this.isUserInput=!1}readOnlyChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.readOnly=this.readOnly,this.validate())}autofocusChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.autofocus=this.autofocus,this.validate())}listChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.setAttribute("list",this.list),this.validate())}maxChanged(e,t){var o;this.max=t<(null!==(o=this.min)&&void 0!==o?o:t)?this.min:t,this.value=this.getValidValue(this.value)}minChanged(e,t){var o;this.min=t>(null!==(o=this.max)&&void 0!==o?o:t)?this.max:t,this.value=this.getValidValue(this.value)}get valueAsNumber(){return new Date(super.value).valueOf()}set valueAsNumber(e){this.value=new Date(e).toString()}get valueAsDate(){return new Date(super.value)}set valueAsDate(e){this.value=e.toString()}valueChanged(e,t){this.value=this.getValidValue(t),t===this.value&&(this.control&&!this.isUserInput&&(this.control.value=this.value),super.valueChanged(e,this.value),void 0===e||this.isUserInput||this.$emit("change"),this.isUserInput=!1)}getValidValue(e){var t,o;let r=new Date(e);return r.toString()===Mr?r="":(r=r>(null!==(t=this.max)&&void 0!==t?t:r)?this.max:r,r=r<(null!==(o=this.min)&&void 0!==o?o:r)?this.min:r,r=`${r.getFullYear().toString().padStart(4,"0")}-${(r.getMonth()+1).toString().padStart(2,"0")}-${r.getDate().toString().padStart(2,"0")}`),r}stepUp(){const e=864e5*this.step,t=new Date(this.value);this.value=new Date(t.toString()!==Mr?t.valueOf()+e:0).toString()}stepDown(){const e=864e5*this.step,t=new Date(this.value);this.value=new Date(t.toString()!==Mr?Math.max(t.valueOf()-e,0):0).toString()}connectedCallback(){super.connectedCallback(),this.validate(),this.control.value=this.value,this.autofocus&&zo.DOM.queueUpdate(()=>{this.focus()}),this.appearance||(this.appearance="outline")}handleTextInput(){this.isUserInput=!0,this.value=this.control.value}handleChange(){this.$emit("change")}handleKeyDown(e){switch(e.key){case u.keyArrowUp:return this.stepUp(),!1;case u.keyArrowDown:return this.stepDown(),!1}return!0}handleBlur(){this.control.value=this.value}}No([zo.attr],Gr.prototype,"appearance",void 0),No([(0,zo.attr)({attribute:"readonly",mode:"boolean"})],Gr.prototype,"readOnly",void 0),No([(0,zo.attr)({mode:"boolean"})],Gr.prototype,"autofocus",void 0),No([zo.attr],Gr.prototype,"list",void 0),No([(0,zo.attr)({converter:zo.nullableNumberConverter})],Gr.prototype,"step",void 0),No([(0,zo.attr)({converter:Er})],Gr.prototype,"max",void 0),No([(0,zo.attr)({converter:Er})],Gr.prototype,"min",void 0),No([zo.observable],Gr.prototype,"defaultSlottedNodes",void 0),(0,h.applyMixins)(Gr,h.StartEnd,h.DelegatesARIATextbox);const _r=zo.css`
  ${(0,h.display)("inline-block")} :host {
    font-family: ${S};
    outline: none;
    user-select: none;
    /* Ensure to display focus highlight */
    margin: calc((${R} - ${O}) * 1px);
  }

  .root {
    box-sizing: border-box;
    position: relative;
    display: flex;
    flex-direction: row;
    color: ${Wt};
    background: ${kt};
    border-radius: calc(${T} * 1px);
    border: calc(${O} * 1px) solid ${Ht};
    height: calc(${Ho} * 1px);
  }

  :host([aria-invalid='true']) .root {
    border-color: ${ro};
  }

  .control {
    -webkit-appearance: none;
    font: inherit;
    background: transparent;
    border: 0;
    color: inherit;
    height: calc(100% - 4px);
    width: 100%;
    margin-top: auto;
    margin-bottom: auto;
    border: none;
    padding: 0 calc(${B} * 2px + 1px);
    font-size: ${I};
    line-height: ${N};
  }

  .control:placeholder-shown {
    text-overflow: ellipsis;
  }

  .control:hover,
  .control:${h.focusVisible},
  .control:disabled,
  .control:active {
    outline: none;
  }

  .label {
    display: block;
    color: ${Wt};
    cursor: pointer;
    font-size: ${I};
    line-height: ${N};
    margin-bottom: 4px;
  }

  .label__hidden {
    display: none;
    visibility: hidden;
  }

  .start,
  .end {
    margin: auto;
    fill: currentcolor;
  }

  ::slotted(svg) {
    /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
    width: 16px;
    height: 16px;
  }

  .start {
    margin-inline-start: 11px;
  }

  .end {
    margin-inline-end: 11px;
  }

  :host(:hover:not([disabled])) .root {
    background: ${wt};
    border-color: ${jt};
  }

  :host([aria-invalid='true']:hover:not([disabled])) .root {
    border-color: ${ao};
  }

  :host(:active:not([disabled])) .root {
    background: ${wt};
    border-color: ${Lt};
  }

  :host([aria-invalid='true']:active:not([disabled])) .root {
    border-color: ${io};
  }

  :host(:focus-within:not([disabled])) .root {
    border-color: ${Qe};
    box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
      ${Qe};
  }

  :host([aria-invalid='true']:focus-within:not([disabled])) .root {
    border-color: ${lo};
    box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
      ${lo};
  }

  :host([appearance='filled']) .root {
    background: ${ft};
  }

  :host([appearance='filled']:hover:not([disabled])) .root {
    background: ${vt};
  }

  :host([disabled]) .label,
  :host([readonly]) .label,
  :host([readonly]) .control,
  :host([disabled]) .control {
    cursor: ${h.disabledCursor};
  }

  :host([disabled]) {
    opacity: ${L};
  }

  :host([disabled]) .control {
    border-color: ${qt};
  }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
    .root,
    :host([appearance='filled']) .root {
      forced-color-adjust: none;
      background: ${u.SystemColors.Field};
      border-color: ${u.SystemColors.FieldText};
    }
    :host([aria-invalid='true']) .root {
      border-style: dashed;
    }
    :host(:hover:not([disabled])) .root,
    :host([appearance='filled']:hover:not([disabled])) .root,
    :host([appearance='filled']:hover) .root {
      background: ${u.SystemColors.Field};
      border-color: ${u.SystemColors.Highlight};
    }
    .start,
    .end {
      fill: currentcolor;
    }
    :host([disabled]) {
      opacity: 1;
    }
    :host([disabled]) .root,
    :host([appearance='filled']:hover[disabled]) .root {
      border-color: ${u.SystemColors.GrayText};
      background: ${u.SystemColors.Field};
    }
    :host(:focus-within:enabled) .root {
      border-color: ${u.SystemColors.Highlight};
      box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
        ${u.SystemColors.Highlight};
    }
    input::placeholder {
      color: ${u.SystemColors.GrayText};
    }
  `)),Wr=(e,t)=>zo.css`
  ${_r}
`,Ur=(e,t)=>zo.html`
  <template class="${e=>e.readOnly?"readonly":""}">
    <label
      part="label"
      for="control"
      class="${e=>e.defaultSlottedNodes&&e.defaultSlottedNodes.length?"label":"label label__hidden"}"
    >
      <slot
        ${(0,zo.slotted)({property:"defaultSlottedNodes",filter:h.whitespaceFilter})}
      ></slot>
    </label>
    <div class="root" part="root">
      ${(0,h.startSlotTemplate)(e,t)}
      <input
        class="control"
        part="control"
        id="control"
        @input="${e=>e.handleTextInput()}"
        @change="${e=>e.handleChange()}"
        ?autofocus="${e=>e.autofocus}"
        ?disabled="${e=>e.disabled}"
        list="${e=>e.list}"
        ?readonly="${e=>e.readOnly}"
        ?required="${e=>e.required}"
        :value="${e=>e.value}"
        type="date"
        aria-atomic="${e=>e.ariaAtomic}"
        aria-busy="${e=>e.ariaBusy}"
        aria-controls="${e=>e.ariaControls}"
        aria-current="${e=>e.ariaCurrent}"
        aria-describedby="${e=>e.ariaDescribedby}"
        aria-details="${e=>e.ariaDetails}"
        aria-disabled="${e=>e.ariaDisabled}"
        aria-errormessage="${e=>e.ariaErrormessage}"
        aria-flowto="${e=>e.ariaFlowto}"
        aria-haspopup="${e=>e.ariaHaspopup}"
        aria-hidden="${e=>e.ariaHidden}"
        aria-invalid="${e=>e.ariaInvalid}"
        aria-keyshortcuts="${e=>e.ariaKeyshortcuts}"
        aria-label="${e=>e.ariaLabel}"
        aria-labelledby="${e=>e.ariaLabelledby}"
        aria-live="${e=>e.ariaLive}"
        aria-owns="${e=>e.ariaOwns}"
        aria-relevant="${e=>e.ariaRelevant}"
        aria-roledescription="${e=>e.ariaRoledescription}"
        ${(0,zo.ref)("control")}
      />
      ${(0,h.endSlotTemplate)(e,t)}
    </div>
  </template>
`,qr=Gr.compose({baseName:"date-field",styles:Wr,template:Ur,shadowOptions:{delegatesFocus:!0}}),Xr={toView:e=>null==e?null:null==e?void 0:e.toColorString(),fromView(e){if(null==e)return null;const t=(0,r.parseColorHexRGB)(e);return t?i.create(t.r,t.g,t.b):null}},Kr=zo.css`
  :host {
    background-color: ${qe};
    color: ${Wt};
  }
`.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
    :host {
      background-color: ${u.SystemColors.ButtonFace};
      box-shadow: 0 0 0 1px ${u.SystemColors.CanvasText};
      color: ${u.SystemColors.ButtonText};
    }
  `));function Yr(e){return(t,o)=>{t[o+"Changed"]=function(t,o){null!=o?e.setValueFor(this,o):e.deleteValueFor(this)}}}class Zr extends h.FoundationElement{constructor(){super(),this.noPaint=!1;const e={handleChange:this.noPaintChanged.bind(this)};zo.Observable.getNotifier(this).subscribe(e,"fillColor"),zo.Observable.getNotifier(this).subscribe(e,"baseLayerLuminance")}noPaintChanged(){this.noPaint||void 0===this.fillColor&&!this.baseLayerLuminance?this.$fastController.removeStyles(Kr):this.$fastController.addStyles(Kr)}}No([(0,zo.attr)({attribute:"no-paint",mode:"boolean"})],Zr.prototype,"noPaint",void 0),No([(0,zo.attr)({attribute:"fill-color",converter:Xr}),Yr(qe)],Zr.prototype,"fillColor",void 0),No([(0,zo.attr)({attribute:"accent-color",converter:Xr,mode:"fromView"}),Yr(je)],Zr.prototype,"accentColor",void 0),No([(0,zo.attr)({attribute:"neutral-color",converter:Xr,mode:"fromView"}),Yr(Be)],Zr.prototype,"neutralColor",void 0),No([(0,zo.attr)({attribute:"error-color",converter:Xr,mode:"fromView"}),Yr(eo)],Zr.prototype,"errorColor",void 0),No([(0,zo.attr)({converter:zo.nullableNumberConverter}),Yr(z)],Zr.prototype,"density",void 0),No([(0,zo.attr)({attribute:"design-unit",converter:zo.nullableNumberConverter}),Yr(B)],Zr.prototype,"designUnit",void 0),No([(0,zo.attr)({attribute:"direction"}),Yr(j)],Zr.prototype,"direction",void 0),No([(0,zo.attr)({attribute:"base-height-multiplier",converter:zo.nullableNumberConverter}),Yr(F)],Zr.prototype,"baseHeightMultiplier",void 0),No([(0,zo.attr)({attribute:"base-horizontal-spacing-multiplier",converter:zo.nullableNumberConverter}),Yr(D)],Zr.prototype,"baseHorizontalSpacingMultiplier",void 0),No([(0,zo.attr)({attribute:"control-corner-radius",converter:zo.nullableNumberConverter}),Yr(T)],Zr.prototype,"controlCornerRadius",void 0),No([(0,zo.attr)({attribute:"stroke-width",converter:zo.nullableNumberConverter}),Yr(O)],Zr.prototype,"strokeWidth",void 0),No([(0,zo.attr)({attribute:"focus-stroke-width",converter:zo.nullableNumberConverter}),Yr(R)],Zr.prototype,"focusStrokeWidth",void 0),No([(0,zo.attr)({attribute:"disabled-opacity",converter:zo.nullableNumberConverter}),Yr(L)],Zr.prototype,"disabledOpacity",void 0),No([(0,zo.attr)({attribute:"type-ramp-minus-2-font-size"}),Yr(E)],Zr.prototype,"typeRampMinus2FontSize",void 0),No([(0,zo.attr)({attribute:"type-ramp-minus-2-line-height"}),Yr(M)],Zr.prototype,"typeRampMinus2LineHeight",void 0),No([(0,zo.attr)({attribute:"type-ramp-minus-1-font-size"}),Yr(A)],Zr.prototype,"typeRampMinus1FontSize",void 0),No([(0,zo.attr)({attribute:"type-ramp-minus-1-line-height"}),Yr(P)],Zr.prototype,"typeRampMinus1LineHeight",void 0),No([(0,zo.attr)({attribute:"type-ramp-base-font-size"}),Yr(I)],Zr.prototype,"typeRampBaseFontSize",void 0),No([(0,zo.attr)({attribute:"type-ramp-base-line-height"}),Yr(N)],Zr.prototype,"typeRampBaseLineHeight",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-1-font-size"}),Yr(G)],Zr.prototype,"typeRampPlus1FontSize",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-1-line-height"}),Yr(_)],Zr.prototype,"typeRampPlus1LineHeight",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-2-font-size"}),Yr(W)],Zr.prototype,"typeRampPlus2FontSize",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-2-line-height"}),Yr(U)],Zr.prototype,"typeRampPlus2LineHeight",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-3-font-size"}),Yr(q)],Zr.prototype,"typeRampPlus3FontSize",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-3-line-height"}),Yr(X)],Zr.prototype,"typeRampPlus3LineHeight",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-4-font-size"}),Yr(K)],Zr.prototype,"typeRampPlus4FontSize",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-4-line-height"}),Yr(Y)],Zr.prototype,"typeRampPlus4LineHeight",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-5-font-size"}),Yr(Z)],Zr.prototype,"typeRampPlus5FontSize",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-5-line-height"}),Yr(J)],Zr.prototype,"typeRampPlus5LineHeight",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-6-font-size"}),Yr(Q)],Zr.prototype,"typeRampPlus6FontSize",void 0),No([(0,zo.attr)({attribute:"type-ramp-plus-6-line-height"}),Yr(ee)],Zr.prototype,"typeRampPlus6LineHeight",void 0),No([(0,zo.attr)({attribute:"accent-fill-rest-delta",converter:zo.nullableNumberConverter}),Yr(te)],Zr.prototype,"accentFillRestDelta",void 0),No([(0,zo.attr)({attribute:"accent-fill-hover-delta",converter:zo.nullableNumberConverter}),Yr(oe)],Zr.prototype,"accentFillHoverDelta",void 0),No([(0,zo.attr)({attribute:"accent-fill-active-delta",converter:zo.nullableNumberConverter}),Yr(re)],Zr.prototype,"accentFillActiveDelta",void 0),No([(0,zo.attr)({attribute:"accent-fill-focus-delta",converter:zo.nullableNumberConverter}),Yr(ae)],Zr.prototype,"accentFillFocusDelta",void 0),No([(0,zo.attr)({attribute:"accent-foreground-rest-delta",converter:zo.nullableNumberConverter}),Yr(ie)],Zr.prototype,"accentForegroundRestDelta",void 0),No([(0,zo.attr)({attribute:"accent-foreground-hover-delta",converter:zo.nullableNumberConverter}),Yr(le)],Zr.prototype,"accentForegroundHoverDelta",void 0),No([(0,zo.attr)({attribute:"accent-foreground-active-delta",converter:zo.nullableNumberConverter}),Yr(se)],Zr.prototype,"accentForegroundActiveDelta",void 0),No([(0,zo.attr)({attribute:"accent-foreground-focus-delta",converter:zo.nullableNumberConverter}),Yr(ne)],Zr.prototype,"accentForegroundFocusDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-rest-delta",converter:zo.nullableNumberConverter}),Yr(ce)],Zr.prototype,"neutralFillRestDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-hover-delta",converter:zo.nullableNumberConverter}),Yr(de)],Zr.prototype,"neutralFillHoverDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-active-delta",converter:zo.nullableNumberConverter}),Yr(he)],Zr.prototype,"neutralFillActiveDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-focus-delta",converter:zo.nullableNumberConverter}),Yr(ue)],Zr.prototype,"neutralFillFocusDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-input-rest-delta",converter:zo.nullableNumberConverter}),Yr(pe)],Zr.prototype,"neutralFillInputRestDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-input-hover-delta",converter:zo.nullableNumberConverter}),Yr(ge)],Zr.prototype,"neutralFillInputHoverDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-input-active-delta",converter:zo.nullableNumberConverter}),Yr(be)],Zr.prototype,"neutralFillInputActiveDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-input-focus-delta",converter:zo.nullableNumberConverter}),Yr(me)],Zr.prototype,"neutralFillInputFocusDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-stealth-rest-delta",converter:zo.nullableNumberConverter}),Yr(fe)],Zr.prototype,"neutralFillStealthRestDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-stealth-hover-delta",converter:zo.nullableNumberConverter}),Yr(ve)],Zr.prototype,"neutralFillStealthHoverDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-stealth-active-delta",converter:zo.nullableNumberConverter}),Yr($e)],Zr.prototype,"neutralFillStealthActiveDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-stealth-focus-delta",converter:zo.nullableNumberConverter}),Yr(xe)],Zr.prototype,"neutralFillStealthFocusDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-strong-hover-delta",converter:zo.nullableNumberConverter}),Yr(ke)],Zr.prototype,"neutralFillStrongHoverDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-strong-active-delta",converter:zo.nullableNumberConverter}),Yr(we)],Zr.prototype,"neutralFillStrongActiveDelta",void 0),No([(0,zo.attr)({attribute:"neutral-fill-strong-focus-delta",converter:zo.nullableNumberConverter}),Yr(Ce)],Zr.prototype,"neutralFillStrongFocusDelta",void 0),No([(0,zo.attr)({attribute:"base-layer-luminance",converter:zo.nullableNumberConverter}),Yr(V)],Zr.prototype,"baseLayerLuminance",void 0),No([(0,zo.attr)({attribute:"neutral-fill-layer-rest-delta",converter:zo.nullableNumberConverter}),Yr(Se)],Zr.prototype,"neutralFillLayerRestDelta",void 0),No([(0,zo.attr)({attribute:"neutral-stroke-divider-rest-delta",converter:zo.nullableNumberConverter}),Yr(ze)],Zr.prototype,"neutralStrokeDividerRestDelta",void 0),No([(0,zo.attr)({attribute:"neutral-stroke-rest-delta",converter:zo.nullableNumberConverter}),Yr(Fe)],Zr.prototype,"neutralStrokeRestDelta",void 0),No([(0,zo.attr)({attribute:"neutral-stroke-hover-delta",converter:zo.nullableNumberConverter}),Yr(De)],Zr.prototype,"neutralStrokeHoverDelta",void 0),No([(0,zo.attr)({attribute:"neutral-stroke-active-delta",converter:zo.nullableNumberConverter}),Yr(Ve)],Zr.prototype,"neutralStrokeActiveDelta",void 0),No([(0,zo.attr)({attribute:"neutral-stroke-focus-delta",converter:zo.nullableNumberConverter}),Yr(Te)],Zr.prototype,"neutralStrokeFocusDelta",void 0);const Jr=(e,t)=>zo.html` <slot></slot> `,Qr=(e,t)=>zo.css`
  ${(0,h.display)("block")}
`,ea=Zr.compose({baseName:"design-system-provider",template:Jr,styles:Qr}),ta=(e,t)=>zo.css`
  :host([hidden]) {
    display: none;
  }

  :host {
    --elevation: 14;
    --dialog-height: 480px;
    --dialog-width: 640px;
    display: block;
  }

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    touch-action: none;
  }

  .positioning-region {
    display: flex;
    justify-content: center;
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    overflow: auto;
  }

  .control {
    ${fr}
    margin-top: auto;
    margin-bottom: auto;
    width: var(--dialog-width);
    height: var(--dialog-height);
    background-color: ${qe};
    z-index: 1;
    border-radius: calc(${T} * 1px);
    border: calc(${O} * 1px) solid transparent;
  }
`;class oa extends h.Dialog{}const ra=oa.compose({baseName:"dialog",baseClass:h.Dialog,template:h.dialogTemplate,styles:ta}),aa=(e,t)=>zo.css`
  .disclosure {
    transition: height 0.35s;
  }

  .disclosure .invoker::-webkit-details-marker {
    display: none;
  }

  .disclosure .invoker {
    list-style-type: none;
  }

  :host([appearance='accent']) .invoker {
    background: ${Ye};
    color: ${ot};
    font-family: ${S};
    font-size: ${I};
    border-radius: calc(${T} * 1px);
    outline: none;
    cursor: pointer;
    margin: 16px 0;
    padding: 12px;
    max-width: max-content;
  }

  :host([appearance='accent']) .invoker:active {
    background: ${Je};
    color: ${at};
  }

  :host([appearance='accent']) .invoker:hover {
    background: ${Ze};
    color: ${rt};
  }

  :host([appearance='lightweight']) .invoker {
    background: transparent;
    color: ${ut};
    border-bottom: calc(${O} * 1px) solid ${ut};
    cursor: pointer;
    width: max-content;
    margin: 16px 0;
  }

  :host([appearance='lightweight']) .invoker:active {
    border-bottom-color: ${gt};
  }

  :host([appearance='lightweight']) .invoker:hover {
    border-bottom-color: ${pt};
  }

  .disclosure[open] .invoker ~ * {
    animation: fadeIn 0.5s ease-in-out;
  }

  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
`;class ia extends h.Disclosure{constructor(){super(...arguments),this.height=0,this.totalHeight=0}connectedCallback(){super.connectedCallback(),this.appearance||(this.appearance="accent")}appearanceChanged(e,t){e!==t&&(this.classList.add(t),this.classList.remove(e))}onToggle(){super.onToggle(),this.details.style.setProperty("height",`${this.disclosureHeight}px`)}setup(){super.setup();const e=()=>this.details.getBoundingClientRect().height;this.show(),this.totalHeight=e(),this.hide(),this.height=e(),this.expanded&&this.show()}get disclosureHeight(){return this.expanded?this.totalHeight:this.height}}No([zo.attr],ia.prototype,"appearance",void 0);const la=ia.compose({baseName:"disclosure",baseClass:h.Disclosure,template:h.disclosureTemplate,styles:aa}),sa=(e,t)=>zo.css`
  ${(0,h.display)("block")} :host {
    box-sizing: content-box;
    height: 0;
    margin: calc(${B} * 1px) 0;
    border-top: calc(${O} * 1px) solid ${Jt};
    border-left: none;
  }

  :host([orientation='vertical']) {
    height: 100%;
    margin: 0 calc(${B} * 1px);
    border-top: none;
    border-left: calc(${O} * 1px) solid ${Jt};
  }
`;class na extends h.Divider{}const ca=na.compose({baseName:"divider",baseClass:h.Divider,template:h.dividerTemplate,styles:sa});class da extends h.ListboxElement{sizeChanged(e,t){super.sizeChanged(e,t),this.updateComputedStylesheet()}updateComputedStylesheet(){this.computedStylesheet&&this.$fastController.removeStyles(this.computedStylesheet);const e=`${this.size}`;this.computedStylesheet=zo.css`
      :host {
        --size: ${e};
      }
    `,this.$fastController.addStyles(this.computedStylesheet)}}const ha=da.compose({baseName:"listbox",baseClass:h.ListboxElement,template:h.listboxTemplate,styles:Sr}),ua=(e,t)=>zo.css`
    ${(0,h.display)("block")} :host {
      --elevation: 11;
      background: ${qe};
      border: calc(${O} * 1px) solid transparent;
      ${fr}
      margin: 0;
      border-radius: calc(${T} * 1px);
      padding: calc(${B} * 1px) 0;
      max-width: 368px;
      min-width: 64px;
    }

    :host([slot='submenu']) {
      width: max-content;
      margin: 0 calc(${B} * 1px);
    }

    ::slotted(hr) {
      box-sizing: content-box;
      height: 0;
      margin: 0;
      border: none;
      border-top: calc(${O} * 1px) solid ${Jt};
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        background: ${u.SystemColors.Canvas};
        border-color: ${u.SystemColors.CanvasText};
      }
    `));class pa extends h.Menu{connectedCallback(){super.connectedCallback(),qe.setValueFor(this,Ne)}}const ga=pa.compose({baseName:"menu",baseClass:h.Menu,template:h.menuTemplate,styles:ua}),ba=(e,t)=>zo.css`
    ${(0,h.display)("grid")} :host {
      contain: layout;
      overflow: visible;
      font-family: ${S};
      outline: none;
      box-sizing: border-box;
      height: calc(${Ho} * 1px);
      grid-template-columns: minmax(42px, auto) 1fr minmax(42px, auto);
      grid-template-rows: auto;
      justify-items: center;
      align-items: center;
      padding: 0;
      margin: 0 calc(${B} * 1px);
      white-space: nowrap;
      background: ${Dt};
      color: ${Wt};
      fill: currentcolor;
      cursor: pointer;
      font-size: ${I};
      line-height: ${N};
      border-radius: calc(${T} * 1px);
      border: calc(${R} * 1px) solid transparent;
    }

    :host(:hover) {
      position: relative;
      z-index: 1;
    }

    :host(.indent-0) {
      grid-template-columns: auto 1fr minmax(42px, auto);
    }
    :host(.indent-0) .content {
      grid-column: 1;
      grid-row: 1;
      margin-inline-start: 10px;
    }
    :host(.indent-0) .expand-collapse-glyph-container {
      grid-column: 5;
      grid-row: 1;
    }
    :host(.indent-2) {
      grid-template-columns:
        minmax(42px, auto) minmax(42px, auto) 1fr minmax(42px, auto)
        minmax(42px, auto);
    }
    :host(.indent-2) .content {
      grid-column: 3;
      grid-row: 1;
      margin-inline-start: 10px;
    }
    :host(.indent-2) .expand-collapse-glyph-container {
      grid-column: 5;
      grid-row: 1;
    }
    :host(.indent-2) .start {
      grid-column: 2;
    }
    :host(.indent-2) .end {
      grid-column: 4;
    }

    :host(:${h.focusVisible}) {
      border-color: ${Qe};
      background: ${zt};
      color: ${Wt};
    }

    :host(:hover) {
      background: ${Vt};
      color: ${Wt};
    }

    :host(:active) {
      background: ${Tt};
    }

    :host([aria-checked='true']),
    :host(.expanded) {
      background: ${ft};
      color: ${Wt};
    }

    :host([disabled]) {
      cursor: ${h.disabledCursor};
      opacity: ${L};
    }

    :host([disabled]:hover) {
      color: ${Wt};
      fill: currentcolor;
      background: ${Dt};
    }

    :host([disabled]:hover) .start,
    :host([disabled]:hover) .end,
    :host([disabled]:hover)::slotted(svg) {
      fill: ${Wt};
    }

    .expand-collapse-glyph {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: calc((16 + ${z}) * 1px);
      height: calc((16 + ${z}) * 1px);
      fill: currentcolor;
    }

    .content {
      grid-column-start: 2;
      justify-self: start;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .start,
    .end {
      display: flex;
      justify-content: center;
    }

    ::slotted(svg) {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: 16px;
      height: 16px;

      /* Something like that would do if the typography is adaptive
      font-size: inherit;
      width: ${G};
      height: ${G};
      */
    }

    :host(:hover) .start,
    :host(:hover) .end,
    :host(:hover)::slotted(svg),
    :host(:active) .start,
    :host(:active) .end,
    :host(:active)::slotted(svg) {
      fill: ${Wt};
    }

    :host(.indent-0[aria-haspopup='menu']) {
      display: grid;
      grid-template-columns: minmax(42px, auto) auto 1fr minmax(42px, auto) minmax(
          42px,
          auto
        );
      align-items: center;
      min-height: 32px;
    }

    :host(.indent-1[aria-haspopup='menu']),
    :host(.indent-1[role='menuitemcheckbox']),
    :host(.indent-1[role='menuitemradio']) {
      display: grid;
      grid-template-columns: minmax(42px, auto) auto 1fr minmax(42px, auto) minmax(
          42px,
          auto
        );
      align-items: center;
      min-height: 32px;
    }

    :host(.indent-2:not([aria-haspopup='menu'])) .end {
      grid-column: 5;
    }

    :host .input-container,
    :host .expand-collapse-glyph-container {
      display: none;
    }

    :host([aria-haspopup='menu']) .expand-collapse-glyph-container,
    :host([role='menuitemcheckbox']) .input-container,
    :host([role='menuitemradio']) .input-container {
      display: grid;
      margin-inline-end: 10px;
    }

    :host([aria-haspopup='menu']) .content,
    :host([role='menuitemcheckbox']) .content,
    :host([role='menuitemradio']) .content {
      grid-column-start: 3;
    }

    :host([aria-haspopup='menu'].indent-0) .content {
      grid-column-start: 1;
    }

    :host([aria-haspopup='menu']) .end,
    :host([role='menuitemcheckbox']) .end,
    :host([role='menuitemradio']) .end {
      grid-column-start: 4;
    }

    :host .expand-collapse,
    :host .checkbox,
    :host .radio {
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      width: 20px;
      height: 20px;
      box-sizing: border-box;
      outline: none;
      margin-inline-start: 10px;
    }

    :host .checkbox,
    :host .radio {
      border: calc(${O} * 1px) solid ${Wt};
    }

    :host([aria-checked='true']) .checkbox,
    :host([aria-checked='true']) .radio {
      background: ${Ye};
      border-color: ${Ye};
    }

    :host .checkbox {
      border-radius: calc(${T} * 1px);
    }

    :host .radio {
      border-radius: 999px;
    }

    :host .checkbox-indicator,
    :host .radio-indicator,
    :host .expand-collapse-indicator,
    ::slotted([slot='checkbox-indicator']),
    ::slotted([slot='radio-indicator']),
    ::slotted([slot='expand-collapse-indicator']) {
      display: none;
    }

    ::slotted([slot='end']:not(svg)) {
      margin-inline-end: 10px;
      color: ${Gt};
    }

    :host([aria-checked='true']) .checkbox-indicator,
    :host([aria-checked='true']) ::slotted([slot='checkbox-indicator']) {
      width: 100%;
      height: 100%;
      display: block;
      fill: ${ot};
      pointer-events: none;
    }

    :host([aria-checked='true']) .radio-indicator {
      position: absolute;
      top: 4px;
      left: 4px;
      right: 4px;
      bottom: 4px;
      border-radius: 999px;
      display: block;
      background: ${ot};
      pointer-events: none;
    }

    :host([aria-checked='true']) ::slotted([slot='radio-indicator']) {
      display: block;
      pointer-events: none;
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        border-color: transparent;
        color: ${u.SystemColors.ButtonText};
        forced-color-adjust: none;
      }

      :host(:hover) {
        background: ${u.SystemColors.Highlight};
        color: ${u.SystemColors.HighlightText};
      }

      :host(:hover) .start,
      :host(:hover) .end,
      :host(:hover)::slotted(svg),
      :host(:active) .start,
      :host(:active) .end,
      :host(:active)::slotted(svg) {
        fill: ${u.SystemColors.HighlightText};
      }

      :host(.expanded) {
        background: ${u.SystemColors.Highlight};
        border-color: ${u.SystemColors.Highlight};
        color: ${u.SystemColors.HighlightText};
      }

      :host(:${h.focusVisible}) {
        background: ${u.SystemColors.Highlight};
        border-color: ${u.SystemColors.ButtonText};
        box-shadow: 0 0 0 calc(${R} * 1px) inset
          ${u.SystemColors.HighlightText};
        color: ${u.SystemColors.HighlightText};
        fill: currentcolor;
      }

      :host([disabled]),
      :host([disabled]:hover),
      :host([disabled]:hover) .start,
      :host([disabled]:hover) .end,
      :host([disabled]:hover)::slotted(svg) {
        background: ${u.SystemColors.Canvas};
        color: ${u.SystemColors.GrayText};
        fill: currentcolor;
        opacity: 1;
      }

      :host .expanded-toggle,
      :host .checkbox,
      :host .radio {
        border-color: ${u.SystemColors.ButtonText};
        background: ${u.SystemColors.HighlightText};
      }

      :host([checked='true']) .checkbox,
      :host([checked='true']) .radio {
        background: ${u.SystemColors.HighlightText};
        border-color: ${u.SystemColors.HighlightText};
      }

      :host(:hover) .expanded-toggle,
            :host(:hover) .checkbox,
            :host(:hover) .radio,
            :host(:${h.focusVisible}) .expanded-toggle,
            :host(:${h.focusVisible}) .checkbox,
            :host(:${h.focusVisible}) .radio,
            :host([checked="true"]:hover) .checkbox,
            :host([checked="true"]:hover) .radio,
            :host([checked="true"]:${h.focusVisible}) .checkbox,
            :host([checked="true"]:${h.focusVisible}) .radio {
        border-color: ${u.SystemColors.HighlightText};
      }

      :host([aria-checked='true']) {
        background: ${u.SystemColors.Highlight};
        color: ${u.SystemColors.HighlightText};
      }

      :host([aria-checked='true']) .checkbox-indicator,
      :host([aria-checked='true']) ::slotted([slot='checkbox-indicator']),
      :host([aria-checked='true']) ::slotted([slot='radio-indicator']) {
        fill: ${u.SystemColors.Highlight};
      }

      :host([aria-checked='true']) .radio-indicator {
        background: ${u.SystemColors.Highlight};
      }

      ::slotted([slot='end']:not(svg)) {
        color: ${u.SystemColors.ButtonText};
      }

      :host(:hover) ::slotted([slot="end"]:not(svg)),
            :host(:${h.focusVisible}) ::slotted([slot="end"]:not(svg)) {
        color: ${u.SystemColors.HighlightText};
      }
    `),new Qo(zo.css`
        .expand-collapse-glyph {
          transform: rotate(0deg);
        }
      `,zo.css`
        .expand-collapse-glyph {
          transform: rotate(180deg);
        }
      `));class ma extends h.MenuItem{}const fa=ma.compose({baseName:"menu-item",baseClass:h.MenuItem,template:h.menuItemTemplate,styles:ba,checkboxIndicator:'\n        <svg\n            part="checkbox-indicator"\n            class="checkbox-indicator"\n            viewBox="0 0 20 20"\n            xmlns="http://www.w3.org/2000/svg"\n        >\n            <path\n                fill-rule="evenodd"\n                clip-rule="evenodd"\n                d="M8.143 12.6697L15.235 4.5L16.8 5.90363L8.23812 15.7667L3.80005 11.2556L5.27591 9.7555L8.143 12.6697Z"\n            />\n        </svg>\n    ',expandCollapseGlyph:'\n        <svg\n            viewBox="0 0 16 16"\n            xmlns="http://www.w3.org/2000/svg"\n            class="expand-collapse-glyph"\n            part="expand-collapse-glyph"\n        >\n            <path\n                d="M5.00001 12.3263C5.00124 12.5147 5.05566 12.699 5.15699 12.8578C5.25831 13.0167 5.40243 13.1437 5.57273 13.2242C5.74304 13.3047 5.9326 13.3354 6.11959 13.3128C6.30659 13.2902 6.4834 13.2152 6.62967 13.0965L10.8988 8.83532C11.0739 8.69473 11.2153 8.51658 11.3124 8.31402C11.4096 8.11146 11.46 7.88966 11.46 7.66499C11.46 7.44033 11.4096 7.21853 11.3124 7.01597C11.2153 6.81341 11.0739 6.63526 10.8988 6.49467L6.62967 2.22347C6.48274 2.10422 6.30501 2.02912 6.11712 2.00691C5.92923 1.9847 5.73889 2.01628 5.56823 2.09799C5.39757 2.17969 5.25358 2.30817 5.153 2.46849C5.05241 2.62882 4.99936 2.8144 5.00001 3.00369V12.3263Z"\n            />\n        </svg>\n    ',radioIndicator:'\n        <span part="radio-indicator" class="radio-indicator"></span>\n    '}),va=(e,t)=>zo.css`
  ${_r}

  .controls {
    opacity: 0;
    margin: auto 0;
  }

  .step-up-glyph,
  .step-down-glyph {
    display: block;
    padding: calc(
        (${B} + 0.5 * ${z} + 0.5 * ${H}) * 1px
      )
      calc((2 + 2 * ${B} + ${z} + ${H}) * 1px);
    cursor: pointer;
  }

  .step-up-glyph:before,
  .step-down-glyph:before {
    content: '';
    display: block;
    border: solid transparent
      calc((2 + ${B} + 0.5 * ${z} + 0.5 * ${H}) * 1px);
  }

  .step-up-glyph:hover:before,
  .step-down-glyph:hover:before {
    background-color: ${vt};
  }

  .step-up-glyph:active:before,
  .step-down-glyph:active:before {
    background-color: ${$t};
  }

  .step-up-glyph:before {
    border-bottom-color: ${Wt};
  }

  .step-down-glyph:before {
    border-top-color: ${Wt};
  }

  :host(:hover:not([disabled])) .controls,
  :host(:focus-within:not([disabled])) .controls {
    opacity: 1;
  }
`;class $a extends h.NumberField{constructor(){super(...arguments),this.appearance="outline"}}No([zo.attr],$a.prototype,"appearance",void 0);const xa=$a.compose({baseName:"number-field",baseClass:h.NumberField,styles:va,template:h.numberFieldTemplate,shadowOptions:{delegatesFocus:!0},stepDownGlyph:'\n        <span class="step-down-glyph" part="step-down-glyph"></span>\n    ',stepUpGlyph:'\n        <span class="step-up-glyph" part="step-up-glyph"></span>\n    '}),ya=(e,t)=>zo.css`
    ${(0,h.display)("inline-flex")} :host {
      align-items: center;
      font-family: ${S};
      border-radius: calc(${T} * 1px);
      border: calc(${R} * 1px) solid transparent;
      box-sizing: border-box;
      background: ${Dt};
      color: ${Wt};
      cursor: pointer;
      flex: 0 0 auto;
      fill: currentcolor;
      font-size: ${I};
      height: calc(${Ho} * 1px);
      line-height: ${N};
      margin: 0 calc((${B} - ${R}) * 1px);
      outline: none;
      overflow: hidden;
      padding: 0 1ch;
      user-select: none;
      white-space: nowrap;
    }

    :host(:not([disabled]):not([aria-selected='true']):hover) {
      background: ${Vt};
    }

    :host(:not([disabled]):not([aria-selected='true']):active) {
      background: ${Tt};
    }

    :host([aria-selected='true']) {
      background: ${Ye};
      color: ${ot};
    }

    :host(:not([disabled])[aria-selected='true']:hover) {
      background: ${Ze};
      color: ${rt};
    }

    :host(:not([disabled])[aria-selected='true']:active) {
      background: ${Je};
      color: ${at};
    }

    :host([disabled]) {
      cursor: ${h.disabledCursor};
      opacity: ${L};
    }

    .content {
      grid-column-start: 2;
      justify-self: start;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .start,
    .end,
    ::slotted(svg) {
      display: flex;
    }

    ::slotted(svg) {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      height: calc(${B} * 4px);
      width: calc(${B} * 4px);
    }

    ::slotted([slot='end']) {
      margin-inline-start: 1ch;
    }

    ::slotted([slot='start']) {
      margin-inline-end: 1ch;
    }

    :host([aria-checked='true'][aria-selected='false']) {
      border-color: ${At};
    }

    :host([aria-checked='true'][aria-selected='true']) {
      border-color: ${At};
      box-shadow: 0 0 0 calc(${R} * 2 * 1px) inset
        ${Et};
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        border-color: transparent;
        forced-color-adjust: none;
        color: ${u.SystemColors.ButtonText};
        fill: currentcolor;
      }

      :host(:not([aria-selected='true']):hover),
      :host([aria-selected='true']) {
        background: ${u.SystemColors.Highlight};
        color: ${u.SystemColors.HighlightText};
      }

      :host([disabled]),
      :host([disabled][aria-selected='false']:hover) {
        background: ${u.SystemColors.Canvas};
        color: ${u.SystemColors.GrayText};
        fill: currentcolor;
        opacity: 1;
      }

      :host([aria-checked='true'][aria-selected='false']) {
        background: ${u.SystemColors.ButtonFace};
        color: ${u.SystemColors.ButtonText};
        border-color: ${u.SystemColors.ButtonText};
      }

      :host([aria-checked='true'][aria-selected='true']),
      :host([aria-checked='true'][aria-selected='true']:hover) {
        background: ${u.SystemColors.Highlight};
        color: ${u.SystemColors.HighlightText};
        border-color: ${u.SystemColors.ButtonText};
      }
    `));class ka extends h.ListboxOption{}const wa=ka.compose({baseName:"option",baseClass:h.ListboxOption,template:h.listboxOptionTemplate,styles:ya}),Ca=(e,t)=>zo.css`
    ${(0,h.display)("flex")} :host {
      align-items: center;
      outline: none;
      height: calc(${B} * 1px);
      margin: calc(${B} * 1px) 0;
    }

    .progress {
      background-color: ${ft};
      border-radius: calc(${B} * 1px);
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      position: relative;
    }

    .determinate {
      background-color: ${ut};
      border-radius: calc(${B} * 1px);
      height: 100%;
      transition: all 0.2s ease-in-out;
      display: flex;
    }

    .indeterminate {
      height: 100%;
      border-radius: calc(${B} * 1px);
      display: flex;
      width: 100%;
      position: relative;
      overflow: hidden;
    }

    .indeterminate-indicator-1 {
      position: absolute;
      opacity: 0;
      height: 100%;
      background-color: ${ut};
      border-radius: calc(${B} * 1px);
      animation-timing-function: cubic-bezier(0.4, 0, 0.6, 1);
      width: 40%;
      animation: indeterminate-1 2s infinite;
    }

    .indeterminate-indicator-2 {
      position: absolute;
      opacity: 0;
      height: 100%;
      background-color: ${ut};
      border-radius: calc(${B} * 1px);
      animation-timing-function: cubic-bezier(0.4, 0, 0.6, 1);
      width: 60%;
      animation: indeterminate-2 2s infinite;
    }

    :host([paused]) .indeterminate-indicator-1,
    :host([paused]) .indeterminate-indicator-2 {
      animation-play-state: paused;
      background-color: ${ft};
    }

    :host([paused]) .determinate {
      background-color: ${Gt};
    }

    @keyframes indeterminate-1 {
      0% {
        opacity: 1;
        transform: translateX(-100%);
      }
      70% {
        opacity: 1;
        transform: translateX(300%);
      }
      70.01% {
        opacity: 0;
      }
      100% {
        opacity: 0;
        transform: translateX(300%);
      }
    }

    @keyframes indeterminate-2 {
      0% {
        opacity: 0;
        transform: translateX(-150%);
      }
      29.99% {
        opacity: 0;
      }
      30% {
        opacity: 1;
        transform: translateX(-150%);
      }
      100% {
        transform: translateX(166.66%);
        opacity: 1;
      }
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      .progress {
        forced-color-adjust: none;
        background-color: ${u.SystemColors.Field};
        box-shadow: 0 0 0 1px inset ${u.SystemColors.FieldText};
      }
      .determinate,
      .indeterminate-indicator-1,
      .indeterminate-indicator-2 {
        forced-color-adjust: none;
        background-color: ${u.SystemColors.FieldText};
      }
      :host([paused]) .determinate,
      :host([paused]) .indeterminate-indicator-1,
      :host([paused]) .indeterminate-indicator-2 {
        background-color: ${u.SystemColors.GrayText};
      }
    `));class Sa extends h.BaseProgress{}const Fa=Sa.compose({baseName:"progress",baseClass:h.BaseProgress,template:h.progressTemplate,styles:Ca,indeterminateIndicator1:'\n        <span class="indeterminate-indicator-1" part="indeterminate-indicator-1"></span>\n    ',indeterminateIndicator2:'\n        <span class="indeterminate-indicator-2" part="indeterminate-indicator-2"></span>\n    '}),Da=(e,t)=>zo.css`
    ${(0,h.display)("flex")} :host {
      align-items: center;
      outline: none;
      height: calc(${Ho} * 1px);
      width: calc(${Ho} * 1px);
      margin: calc(${Ho} * 1px) 0;
    }

    .progress {
      height: 100%;
      width: 100%;
    }

    .background {
      stroke: ${ft};
      fill: none;
      stroke-width: 2px;
    }

    .determinate {
      stroke: ${ut};
      fill: none;
      stroke-width: 2px;
      stroke-linecap: round;
      transform-origin: 50% 50%;
      transform: rotate(-90deg);
      transition: all 0.2s ease-in-out;
    }

    .indeterminate-indicator-1 {
      stroke: ${ut};
      fill: none;
      stroke-width: 2px;
      stroke-linecap: round;
      transform-origin: 50% 50%;
      transform: rotate(-90deg);
      transition: all 0.2s ease-in-out;
      animation: spin-infinite 2s linear infinite;
    }

    :host([paused]) .indeterminate-indicator-1 {
      animation-play-state: paused;
      stroke: ${ft};
    }

    :host([paused]) .determinate {
      stroke: ${Gt};
    }

    @keyframes spin-infinite {
      0% {
        stroke-dasharray: 0.01px 43.97px;
        transform: rotate(0deg);
      }
      50% {
        stroke-dasharray: 21.99px 21.99px;
        transform: rotate(450deg);
      }
      100% {
        stroke-dasharray: 0.01px 43.97px;
        transform: rotate(1080deg);
      }
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      .indeterminate-indicator-1,
      .determinate {
        stroke: ${u.SystemColors.FieldText};
      }
      .background {
        stroke: ${u.SystemColors.Field};
      }
      :host([paused]) .indeterminate-indicator-1 {
        stroke: ${u.SystemColors.Field};
      }
      :host([paused]) .determinate {
        stroke: ${u.SystemColors.GrayText};
      }
    `));class Va extends h.BaseProgress{}const Ta=Va.compose({baseName:"progress-ring",baseClass:h.BaseProgress,template:h.progressRingTemplate,styles:Da,indeterminateIndicator:'\n        <svg class="progress" part="progress" viewBox="0 0 16 16">\n            <circle\n                class="background"\n                part="background"\n                cx="8px"\n                cy="8px"\n                r="7px"\n            ></circle>\n            <circle\n                class="indeterminate-indicator-1"\n                part="indeterminate-indicator-1"\n                cx="8px"\n                cy="8px"\n                r="7px"\n            ></circle>\n        </svg>\n    '}),za=(e,t)=>zo.css`
    ${(0,h.display)("inline-flex")} :host {
      --input-size: calc((${Ho} / 2) + ${B});
      align-items: center;
      outline: none;
      margin: calc(${B} * 1px) 0;
      /* Chromium likes to select label text or the default slot when
                the radio is clicked. Maybe there is a better solution here? */
      user-select: none;
      position: relative;
      flex-direction: row;
      transition: all 0.2s ease-in-out;
    }

    .control {
      position: relative;
      width: calc((${Ho} / 2 + ${B}) * 1px);
      height: calc((${Ho} / 2 + ${B}) * 1px);
      box-sizing: border-box;
      border-radius: 999px;
      border: calc(${O} * 1px) solid ${qt};
      background: ${kt};
      outline: none;
      cursor: pointer;
    }

    :host([aria-invalid='true']) .control {
      border-color: ${ro};
    }

    .label {
      font-family: ${S};
      color: ${Wt};
      padding-inline-start: calc(${B} * 2px + 2px);
      margin-inline-end: calc(${B} * 2px + 2px);
      cursor: pointer;
      font-size: ${I};
      line-height: ${N};
    }

    .label__hidden {
      display: none;
      visibility: hidden;
    }

    .control,
    .checked-indicator {
      flex-shrink: 0;
    }

    .checked-indicator {
      position: absolute;
      top: 5px;
      left: 5px;
      right: 5px;
      bottom: 5px;
      border-radius: 999px;
      display: inline-block;
      background: ${ot};
      fill: ${ot};
      opacity: 0;
      pointer-events: none;
    }

    :host(:not([disabled])) .control:hover {
      background: ${wt};
      border-color: ${Xt};
    }

    :host([aria-invalid='true']:not([disabled])) .control:hover {
      border-color: ${ao};
    }

    :host(:not([disabled])) .control:active {
      background: ${Ct};
      border-color: ${Kt};
    }

    :host([aria-invalid='true']:not([disabled])) .control:active {
      border-color: ${io};
    }

    :host(:${h.focusVisible}) .control {
      outline: solid calc(${R} * 1px) ${Qe};
    }

    :host([aria-invalid='true']:${h.focusVisible}) .control {
      outline-color: ${lo};
    }

    :host([aria-checked='true']) .control {
      background: ${Ye};
      border: calc(${O} * 1px) solid ${Ye};
    }

    :host([aria-invalid='true'][aria-checked='true']) .control {
      background-color: ${ro};
      border-color: ${ro};
    }

    :host([aria-checked='true']:not([disabled])) .control:hover {
      background: ${Ze};
      border: calc(${O} * 1px) solid ${Ze};
    }

    :host([aria-invalid='true'][aria-checked='true']:not([disabled]))
      .control:hover {
      background-color: ${ao};
      border-color: ${ao};
    }

    :host([aria-checked='true']:not([disabled]))
      .control:hover
      .checked-indicator {
      background: ${rt};
      fill: ${rt};
    }

    :host([aria-checked='true']:not([disabled])) .control:active {
      background: ${Je};
      border: calc(${O} * 1px) solid ${Je};
    }

    :host([aria-invalid='true'][aria-checked='true']:not([disabled]))
      .control:active {
      background-color: ${io};
      border-color: ${io};
    }

    :host([aria-checked='true']:not([disabled]))
      .control:active
      .checked-indicator {
      background: ${at};
      fill: ${at};
    }

    :host([aria-checked="true"]:${h.focusVisible}:not([disabled])) .control {
      outline-offset: 2px;
      outline: solid calc(${R} * 1px) ${Qe};
    }

    :host([aria-invalid='true'][aria-checked="true"]:${h.focusVisible}:not([disabled])) .control {
      outline-color: ${lo};
    }

    :host([disabled]) .label,
    :host([readonly]) .label,
    :host([readonly]) .control,
    :host([disabled]) .control {
      cursor: ${h.disabledCursor};
    }

    :host([aria-checked='true']) .checked-indicator {
      opacity: 1;
    }

    :host([disabled]) {
      opacity: ${L};
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      .control,
      :host([aria-checked='true']:not([disabled])) .control {
        forced-color-adjust: none;
        border-color: ${u.SystemColors.FieldText};
        background: ${u.SystemColors.Field};
      }
      :host([aria-invalid='true']) {
        border-style: dashed;
      }
      :host(:not([disabled])) .control:hover {
        border-color: ${u.SystemColors.Highlight};
        background: ${u.SystemColors.Field};
      }
      :host([aria-checked='true']:not([disabled])) .control:hover,
      :host([aria-checked='true']:not([disabled])) .control:active {
        border-color: ${u.SystemColors.Highlight};
        background: ${u.SystemColors.Highlight};
      }
      :host([aria-checked='true']) .checked-indicator {
        background: ${u.SystemColors.Highlight};
        fill: ${u.SystemColors.Highlight};
      }
      :host([aria-checked='true']:not([disabled]))
        .control:hover
        .checked-indicator,
      :host([aria-checked='true']:not([disabled]))
        .control:active
        .checked-indicator {
        background: ${u.SystemColors.HighlightText};
        fill: ${u.SystemColors.HighlightText};
      }
      :host(:${h.focusVisible}) .control {
        border-color: ${u.SystemColors.Highlight};
        outline-offset: 2px;
        outline: solid calc(${R} * 1px) ${u.SystemColors.FieldText};
      }
      :host([aria-checked="true"]:${h.focusVisible}:not([disabled])) .control {
        border-color: ${u.SystemColors.Highlight};
        outline: solid calc(${R} * 1px) ${u.SystemColors.FieldText};
      }
      :host([disabled]) {
        forced-color-adjust: none;
        opacity: 1;
      }
      :host([disabled]) .label {
        color: ${u.SystemColors.GrayText};
      }
      :host([disabled]) .control,
      :host([aria-checked='true'][disabled]) .control:hover,
      .control:active {
        background: ${u.SystemColors.Field};
        border-color: ${u.SystemColors.GrayText};
      }
      :host([disabled]) .checked-indicator,
      :host([aria-checked='true'][disabled]) .control:hover .checked-indicator {
        fill: ${u.SystemColors.GrayText};
        background: ${u.SystemColors.GrayText};
      }
    `)),Ba=(e,t)=>zo.html`
  <template
    role="radio"
    aria-checked="${e=>e.checked}"
    aria-required="${e=>e.required}"
    aria-disabled="${e=>e.disabled}"
    aria-readonly="${e=>e.readOnly}"
    @keypress="${(e,t)=>e.keypressHandler(t.event)}"
    @click="${(e,t)=>e.clickHandler(t.event)}"
  >
    <div part="control" class="control">
      <slot name="checked-indicator">
        ${t.checkedIndicator||""}
      </slot>
    </div>
    <label
      part="label"
      class="${e=>e.defaultSlottedNodes&&e.defaultSlottedNodes.length?"label":"label label__hidden"}"
    >
      <slot ${(0,zo.slotted)("defaultSlottedNodes")}></slot>
    </label>
  </template>
`;class Ha extends h.Radio{}const ja=Ha.compose({baseName:"radio",baseClass:h.Radio,template:Ba,styles:za,checkedIndicator:'\n        <div part="checked-indicator" class="checked-indicator"></div>\n    '}),La=(e,t)=>zo.css`
  ${(0,h.display)("flex")} :host {
    align-items: flex-start;
    margin: calc(${B} * 1px) 0;
    flex-direction: column;
  }
  .positioning-region {
    display: flex;
    flex-wrap: wrap;
  }
  :host([orientation='vertical']) .positioning-region {
    flex-direction: column;
  }
  :host([orientation='horizontal']) .positioning-region {
    flex-direction: row;
  }
`;class Oa extends h.RadioGroup{constructor(){super();const e=zo.Observable.getNotifier(this),t={handleChange(e,t){"slottedRadioButtons"===t&&e.ariaInvalidChanged()}};e.subscribe(t,"slottedRadioButtons")}ariaInvalidChanged(){this.slottedRadioButtons&&this.slottedRadioButtons.forEach(e=>{var t;e.setAttribute("aria-invalid",null!==(t=this.getAttribute("aria-invalid"))&&void 0!==t?t:"false")})}}const Ra=Oa.compose({baseName:"radio-group",baseClass:h.RadioGroup,template:h.radioGroupTemplate,styles:La}),Ia=h.DesignToken.create("clear-button-hover").withDefault(e=>{const t=Ft.getValueFor(e),o=mt.getValueFor(e);return t.evaluate(e,o.evaluate(e).hover).hover}),Na=h.DesignToken.create("clear-button-active").withDefault(e=>{const t=Ft.getValueFor(e),o=mt.getValueFor(e);return t.evaluate(e,o.evaluate(e).hover).active}),Aa=(e,t)=>zo.css`
  ${_r}

  .control::-webkit-search-cancel-button {
    -webkit-appearance: none;
  }

  .control:hover,
    .control:${h.focusVisible},
    .control:disabled,
    .control:active {
    outline: none;
  }

  .clear-button {
    height: calc(100% - 2px);
    opacity: 0;
    margin: 1px;
    background: transparent;
    color: ${Wt};
    fill: currentcolor;
    border: none;
    border-radius: calc(${T} * 1px);
    min-width: calc(${Ho} * 1px);
    font-size: ${I};
    line-height: ${N};
    outline: none;
    font-family: ${S};
    padding: 0 calc((10 + (${B} * 2 * ${z})) * 1px);
  }

  .clear-button:hover {
    background: ${Vt};
  }

  .clear-button:active {
    background: ${Tt};
  }

  :host([appearance='filled']) .clear-button:hover {
    background: ${Ia};
  }

  :host([appearance='filled']) .clear-button:active {
    background: ${Na};
  }

  .input-wrapper {
    display: flex;
    position: relative;
    width: 100%;
  }

  .start,
  .end {
    display: flex;
    margin: 1px;
    fill: currentcolor;
  }

  ::slotted([slot='end']) {
    height: 100%;
  }

  .end {
    margin-inline-end: 1px;
    height: calc(100% - 2px);
  }

  ::slotted(svg) {
    /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
    width: 16px;
    height: 16px;
    margin-inline-end: 11px;
    margin-inline-start: 11px;
    margin-top: auto;
    margin-bottom: auto;
  }

  .clear-button__hidden {
    opacity: 0;
  }

  :host(:hover:not([disabled], [readOnly])) .clear-button,
  :host(:active:not([disabled], [readOnly])) .clear-button,
  :host(:focus-within:not([disabled], [readOnly])) .clear-button {
    opacity: 1;
  }

  :host(:hover:not([disabled], [readOnly])) .clear-button__hidden,
  :host(:active:not([disabled], [readOnly])) .clear-button__hidden,
  :host(:focus-within:not([disabled], [readOnly])) .clear-button__hidden {
    opacity: 0;
  }
`;class Pa extends h.Search{constructor(){super(...arguments),this.appearance="outline"}}No([zo.attr],Pa.prototype,"appearance",void 0);const Ea=Pa.compose({baseName:"search",baseClass:h.Search,template:h.searchTemplate,styles:Aa,shadowOptions:{delegatesFocus:!0}});class Ma extends h.Select{constructor(){super(...arguments),this.listboxScrollWidth=""}autoWidthChanged(e,t){t?this.setAutoWidth():this.style.removeProperty("width")}setAutoWidth(){if(!this.autoWidth||!this.isConnected)return;let e=this.listbox.getBoundingClientRect().width;0===e&&this.listbox.hidden&&(Object.assign(this.listbox.style,{visibility:"hidden"}),this.listbox.removeAttribute("hidden"),e=this.listbox.getBoundingClientRect().width,this.listbox.setAttribute("hidden",""),this.listbox.style.removeProperty("visibility")),e>0&&Object.assign(this.style,{width:`${e}px`})}connectedCallback(){super.connectedCallback(),this.setAutoWidth(),this.listbox&&qe.setValueFor(this.listbox,Ne)}slottedOptionsChanged(e,t){super.slottedOptionsChanged(e,t),this.setAutoWidth()}get listboxMaxHeight(){return Math.floor(this.maxHeight/Qt.getValueFor(this)).toString()}listboxScrollWidthChanged(){this.updateComputedStylesheet()}get selectSize(){var e;return`${null!==(e=this.size)&&void 0!==e?e:this.multiple?4:0}`}multipleChanged(e,t){super.multipleChanged(e,t),this.updateComputedStylesheet()}maxHeightChanged(e,t){this.collapsible&&this.updateComputedStylesheet()}setPositioning(){super.setPositioning(),this.updateComputedStylesheet()}sizeChanged(e,t){super.sizeChanged(e,t),this.updateComputedStylesheet(),this.collapsible?requestAnimationFrame(()=>{this.listbox.style.setProperty("display","flex"),this.listbox.style.setProperty("overflow","visible"),this.listbox.style.setProperty("visibility","hidden"),this.listbox.style.setProperty("width","auto"),this.listbox.hidden=!1,this.listboxScrollWidth=`${this.listbox.scrollWidth}`,this.listbox.hidden=!0,this.listbox.style.removeProperty("display"),this.listbox.style.removeProperty("overflow"),this.listbox.style.removeProperty("visibility"),this.listbox.style.removeProperty("width")}):this.listboxScrollWidth=""}updateComputedStylesheet(){this.computedStylesheet&&this.$fastController.removeStyles(this.computedStylesheet),this.computedStylesheet=zo.css`
      :host {
        --listbox-max-height: ${this.listboxMaxHeight};
        --listbox-scroll-width: ${this.listboxScrollWidth};
        --size: ${this.selectSize};
      }
    `,this.$fastController.addStyles(this.computedStylesheet)}}No([(0,zo.attr)({attribute:"autowidth",mode:"boolean"})],Ma.prototype,"autoWidth",void 0),No([(0,zo.attr)({attribute:"minimal",mode:"boolean"})],Ma.prototype,"minimal",void 0),No([zo.attr],Ma.prototype,"scale",void 0),No([zo.observable],Ma.prototype,"listboxScrollWidth",void 0);const Ga=Ma.compose({baseName:"select",baseClass:h.Select,template:h.selectTemplate,styles:Fr,indicator:'\n        <svg\n            class="select-indicator"\n            part="select-indicator"\n            viewBox="0 0 12 7"\n            xmlns="http://www.w3.org/2000/svg"\n        >\n            <path\n                d="M11.85.65c.2.2.2.5 0 .7L6.4 6.84a.55.55 0 01-.78 0L.14 1.35a.5.5 0 11.71-.7L6 5.8 11.15.65c.2-.2.5-.2.7 0z"\n            />\n        </svg>\n    '}),_a=(e,t)=>zo.css`
    ${(0,h.display)("block")} :host {
      --skeleton-fill-default: #e1dfdd;
      overflow: hidden;
      width: 100%;
      position: relative;
      background-color: var(--skeleton-fill, var(--skeleton-fill-default));
      --skeleton-animation-gradient-default: linear-gradient(
        270deg,
        var(--skeleton-fill, var(--skeleton-fill-default)) 0%,
        #f3f2f1 51.13%,
        var(--skeleton-fill, var(--skeleton-fill-default)) 100%
      );
      --skeleton-animation-timing-default: ease-in-out;
    }

    :host([shape='rect']) {
      border-radius: calc(${T} * 1px);
    }

    :host([shape='circle']) {
      border-radius: 100%;
      overflow: hidden;
    }

    object {
      position: absolute;
      width: 100%;
      height: auto;
      z-index: 2;
    }

    object img {
      width: 100%;
      height: auto;
    }

    ${(0,h.display)("block")} span.shimmer {
      position: absolute;
      width: 100%;
      height: 100%;
      background-image: var(
        --skeleton-animation-gradient,
        var(--skeleton-animation-gradient-default)
      );
      background-size: 0px 0px / 90% 100%;
      background-repeat: no-repeat;
      background-color: var(--skeleton-animation-fill, ${ft});
      animation: shimmer 2s infinite;
      animation-timing-function: var(
        --skeleton-animation-timing,
        var(--skeleton-timing-default)
      );
      animation-direction: normal;
      z-index: 1;
    }

    ::slotted(svg) {
      z-index: 2;
    }

    ::slotted(.pattern) {
      width: 100%;
      height: 100%;
    }

    @keyframes shimmer {
      0% {
        transform: translateX(-100%);
      }
      100% {
        transform: translateX(100%);
      }
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        forced-color-adjust: none;
        background-color: ${u.SystemColors.ButtonFace};
        box-shadow: 0 0 0 1px ${u.SystemColors.ButtonText};
      }

      ${(0,h.display)("block")} span.shimmer {
        display: none;
      }
    `));class Wa extends h.Skeleton{}const Ua=Wa.compose({baseName:"skeleton",baseClass:h.Skeleton,template:h.skeletonTemplate,styles:_a}),qa=zo.css`
  .track-start {
    left: 0;
  }
`,Xa=zo.css`
  .track-start {
    right: 0;
  }
`,Ka=(e,t)=>zo.css`
    :host([hidden]) {
      display: none;
    }

    ${(0,h.display)("inline-grid")} :host {
      --thumb-size: calc(${Ho} * 0.5 - ${B});
      --thumb-translate: calc(
        var(--thumb-size) * -0.5 + var(--track-width) / 2
      );
      --track-overhang: calc((${B} / 2) * -1);
      --track-width: ${B};
      --jp-slider-height: calc(var(--thumb-size) * 10);
      align-items: center;
      width: 100%;
      margin: calc(${B} * 1px) 0;
      user-select: none;
      box-sizing: border-box;
      border-radius: calc(${T} * 1px);
      outline: none;
      cursor: pointer;
    }
    :host([orientation='horizontal']) .positioning-region {
      position: relative;
      margin: 0 8px;
      display: grid;
      grid-template-rows: calc(var(--thumb-size) * 1px) 1fr;
    }
    :host([orientation='vertical']) .positioning-region {
      position: relative;
      margin: 0 8px;
      display: grid;
      height: 100%;
      grid-template-columns: calc(var(--thumb-size) * 1px) 1fr;
    }

    :host(:${h.focusVisible}) .thumb-cursor {
      box-shadow:
        0 0 0 2px ${qe},
        0 0 0 calc((2 + ${R}) * 1px) ${Qe};
    }

    :host([aria-invalid='true']:${h.focusVisible}) .thumb-cursor {
      box-shadow:
        0 0 0 2px ${qe},
        0 0 0 calc((2 + ${R}) * 1px) ${lo};
    }

    .thumb-container {
      position: absolute;
      height: calc(var(--thumb-size) * 1px);
      width: calc(var(--thumb-size) * 1px);
      transition: all 0.2s ease;
      color: ${Wt};
      fill: currentcolor;
    }
    .thumb-cursor {
      border: none;
      width: calc(var(--thumb-size) * 1px);
      height: calc(var(--thumb-size) * 1px);
      background: ${Wt};
      border-radius: calc(${T} * 1px);
    }
    .thumb-cursor:hover {
      background: ${Wt};
      border-color: ${Xt};
    }
    .thumb-cursor:active {
      background: ${Wt};
    }
    .track-start {
      background: ${ut};
      position: absolute;
      height: 100%;
      left: 0;
      border-radius: calc(${T} * 1px);
    }
    :host([aria-invalid='true']) .track-start {
      background-color: ${ro};
    }
    :host([orientation='horizontal']) .thumb-container {
      transform: translateX(calc(var(--thumb-size) * 0.5px))
        translateY(calc(var(--thumb-translate) * 1px));
    }
    :host([orientation='vertical']) .thumb-container {
      transform: translateX(calc(var(--thumb-translate) * 1px))
        translateY(calc(var(--thumb-size) * 0.5px));
    }
    :host([orientation='horizontal']) {
      min-width: calc(var(--thumb-size) * 1px);
    }
    :host([orientation='horizontal']) .track {
      right: calc(var(--track-overhang) * 1px);
      left: calc(var(--track-overhang) * 1px);
      align-self: start;
      height: calc(var(--track-width) * 1px);
    }
    :host([orientation='vertical']) .track {
      top: calc(var(--track-overhang) * 1px);
      bottom: calc(var(--track-overhang) * 1px);
      width: calc(var(--track-width) * 1px);
      height: 100%;
    }
    .track {
      background: ${qt};
      position: absolute;
      border-radius: calc(${T} * 1px);
    }
    :host([orientation='vertical']) {
      height: calc(var(--fast-slider-height) * 1px);
      min-height: calc(var(--thumb-size) * 1px);
      min-width: calc(${B} * 20px);
    }
    :host([orientation='vertical']) .track-start {
      height: auto;
      width: 100%;
      top: 0;
    }
    :host([disabled]),
    :host([readonly]) {
      cursor: ${h.disabledCursor};
    }
    :host([disabled]) {
      opacity: ${L};
    }
  `.withBehaviors(new Qo(qa,Xa),(0,h.forcedColorsStylesheetBehavior)(zo.css`
      .thumb-cursor {
        forced-color-adjust: none;
        border-color: ${u.SystemColors.FieldText};
        background: ${u.SystemColors.FieldText};
      }
      .thumb-cursor:hover,
      .thumb-cursor:active {
        background: ${u.SystemColors.Highlight};
      }
      .track {
        forced-color-adjust: none;
        background: ${u.SystemColors.FieldText};
      }
      :host(:${h.focusVisible}) .thumb-cursor {
        border-color: ${u.SystemColors.Highlight};
      }
      :host([disabled]) {
        opacity: 1;
      }
      :host([disabled]) .track,
      :host([disabled]) .thumb-cursor {
        forced-color-adjust: none;
        background: ${u.SystemColors.GrayText};
      }

      :host(:${h.focusVisible}) .thumb-cursor {
        background: ${u.SystemColors.Highlight};
        border-color: ${u.SystemColors.Highlight};
        box-shadow:
          0 0 0 2px ${u.SystemColors.Field},
          0 0 0 4px ${u.SystemColors.FieldText};
      }
    `));class Ya extends h.Slider{}const Za=Ya.compose({baseName:"slider",baseClass:h.Slider,template:h.sliderTemplate,styles:Ka,thumb:'\n        <div class="thumb-cursor"></div>\n    '}),Ja=zo.css`
  :host {
    align-self: start;
    grid-row: 2;
    margin-top: -2px;
    height: calc((${Ho} / 2 + ${B}) * 1px);
    width: auto;
  }
  .container {
    grid-template-rows: auto auto;
    grid-template-columns: 0;
  }
  .label {
    margin: 2px 0;
  }
`,Qa=zo.css`
  :host {
    justify-self: start;
    grid-column: 2;
    margin-left: 2px;
    height: auto;
    width: calc((${Ho} / 2 + ${B}) * 1px);
  }
  .container {
    grid-template-columns: auto auto;
    grid-template-rows: 0;
    min-width: calc(var(--thumb-size) * 1px);
    height: calc(var(--thumb-size) * 1px);
  }
  .mark {
    transform: rotate(90deg);
    align-self: center;
  }
  .label {
    margin-left: calc((${B} / 2) * 3px);
    align-self: center;
  }
`,ei=(e,t)=>zo.css`
    ${(0,h.display)("block")} :host {
      font-family: ${S};
      color: ${Wt};
      fill: currentcolor;
    }
    .root {
      position: absolute;
      display: grid;
    }
    .container {
      display: grid;
      justify-self: center;
    }
    .label {
      justify-self: center;
      align-self: center;
      white-space: nowrap;
      max-width: 30px;
    }
    .mark {
      width: calc((${B} / 4) * 1px);
      height: calc(${Ho} * 0.25 * 1px);
      background: ${qt};
      justify-self: center;
    }
    :host(.disabled) {
      opacity: ${L};
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      .mark {
        forced-color-adjust: none;
        background: ${u.SystemColors.FieldText};
      }
      :host(.disabled) {
        forced-color-adjust: none;
        opacity: 1;
      }
      :host(.disabled) .label {
        color: ${u.SystemColors.GrayText};
      }
      :host(.disabled) .mark {
        background: ${u.SystemColors.GrayText};
      }
    `));class ti extends h.SliderLabel{sliderOrientationChanged(){this.sliderOrientation===u.Orientation.horizontal?(this.$fastController.addStyles(Ja),this.$fastController.removeStyles(Qa)):(this.$fastController.addStyles(Qa),this.$fastController.removeStyles(Ja))}}const oi=ti.compose({baseName:"slider-label",baseClass:h.SliderLabel,template:h.sliderLabelTemplate,styles:ei}),ri=(e,t)=>zo.css`
    :host([hidden]) {
      display: none;
    }

    ${(0,h.display)("inline-flex")} :host {
      align-items: center;
      outline: none;
      font-family: ${S};
      margin: calc(${B} * 1px) 0;
      ${""} user-select: none;
    }

    :host([disabled]) {
      opacity: ${L};
    }

    :host([disabled]) .label,
    :host([readonly]) .label,
    :host([readonly]) .switch,
    :host([disabled]) .switch {
      cursor: ${h.disabledCursor};
    }

    .switch {
      position: relative;
      outline: none;
      box-sizing: border-box;
      width: calc(${Ho} * 1px);
      height: calc((${Ho} / 2 + ${B}) * 1px);
      background: ${kt};
      border-radius: calc(${T} * 1px);
      border: calc(${O} * 1px) solid ${qt};
    }

    :host([aria-invalid='true']) .switch {
      border-color: ${ro};
    }

    .switch:hover {
      background: ${wt};
      border-color: ${Xt};
      cursor: pointer;
    }

    :host([disabled]) .switch:hover,
    :host([readonly]) .switch:hover {
      background: ${wt};
      border-color: ${Xt};
      cursor: ${h.disabledCursor};
    }

    :host([aria-invalid='true'][disabled]) .switch:hover,
    :host([aria-invalid='true'][readonly]) .switch:hover {
      border-color: ${ao};
    }

    :host(:not([disabled])) .switch:active {
      background: ${Ct};
      border-color: ${Kt};
    }

    :host([aria-invalid='true']:not([disabled])) .switch:active {
      border-color: ${io};
    }

    :host(:${h.focusVisible}) .switch {
      outline-offset: 2px;
      outline: solid calc(${R} * 1px) ${Qe};
    }

    :host([aria-invalid='true']:${h.focusVisible}) .switch {
      outline-color: ${lo};
    }

    .checked-indicator {
      position: absolute;
      top: 5px;
      bottom: 5px;
      background: ${Wt};
      border-radius: calc(${T} * 1px);
      transition: all 0.2s ease-in-out;
    }

    .status-message {
      color: ${Wt};
      cursor: pointer;
      font-size: ${I};
      line-height: ${N};
    }

    :host([disabled]) .status-message,
    :host([readonly]) .status-message {
      cursor: ${h.disabledCursor};
    }

    .label {
      color: ${Wt};
      margin-inline-end: calc(${B} * 2px + 2px);
      font-size: ${I};
      line-height: ${N};
      cursor: pointer;
    }

    .label__hidden {
      display: none;
      visibility: hidden;
    }

    ::slotted([slot='checked-message']),
    ::slotted([slot='unchecked-message']) {
      margin-inline-start: calc(${B} * 2px + 2px);
    }

    :host([aria-checked='true']) .checked-indicator {
      background: ${ot};
    }

    :host([aria-checked='true']) .switch {
      background: ${Ye};
      border-color: ${Ye};
    }

    :host([aria-checked='true']:not([disabled])) .switch:hover {
      background: ${Ze};
      border-color: ${Ze};
    }

    :host([aria-invalid='true'][aria-checked='true']) .switch {
      background-color: ${ro};
      border-color: ${ro};
    }

    :host([aria-invalid='true'][aria-checked='true']:not([disabled]))
      .switch:hover {
      background-color: ${ao};
      border-color: ${ao};
    }

    :host([aria-checked='true']:not([disabled]))
      .switch:hover
      .checked-indicator {
      background: ${rt};
    }

    :host([aria-checked='true']:not([disabled])) .switch:active {
      background: ${Je};
      border-color: ${Je};
    }

    :host([aria-invalid='true'][aria-checked='true']:not([disabled]))
      .switch:active {
      background-color: ${io};
      border-color: ${io};
    }

    :host([aria-checked='true']:not([disabled]))
      .switch:active
      .checked-indicator {
      background: ${at};
    }

    :host([aria-checked="true"]:${h.focusVisible}:not([disabled])) .switch {
      outline: solid calc(${R} * 1px) ${Qe};
    }

    :host([aria-invalid='true'][aria-checked="true"]:${h.focusVisible}:not([disabled])) .switch {
      outline-color: ${lo};
    }

    .unchecked-message {
      display: block;
    }

    .checked-message {
      display: none;
    }

    :host([aria-checked='true']) .unchecked-message {
      display: none;
    }

    :host([aria-checked='true']) .checked-message {
      display: block;
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      .checked-indicator,
      :host(:not([disabled])) .switch:active .checked-indicator {
        forced-color-adjust: none;
        background: ${u.SystemColors.FieldText};
      }
      .switch {
        forced-color-adjust: none;
        background: ${u.SystemColors.Field};
        border-color: ${u.SystemColors.FieldText};
      }
      :host([aria-invalid='true']) .switch {
        border-style: dashed;
      }
      :host(:not([disabled])) .switch:hover {
        background: ${u.SystemColors.HighlightText};
        border-color: ${u.SystemColors.Highlight};
      }
      :host([aria-checked='true']) .switch {
        background: ${u.SystemColors.Highlight};
        border-color: ${u.SystemColors.Highlight};
      }
      :host([aria-checked='true']:not([disabled])) .switch:hover,
      :host(:not([disabled])) .switch:active {
        background: ${u.SystemColors.HighlightText};
        border-color: ${u.SystemColors.Highlight};
      }
      :host([aria-checked='true']) .checked-indicator {
        background: ${u.SystemColors.HighlightText};
      }
      :host([aria-checked='true']:not([disabled]))
        .switch:hover
        .checked-indicator {
        background: ${u.SystemColors.Highlight};
      }
      :host([disabled]) {
        opacity: 1;
      }
      :host(:${h.focusVisible}) .switch {
        border-color: ${u.SystemColors.Highlight};
        outline-offset: 2px;
        outline: solid calc(${R} * 1px) ${u.SystemColors.FieldText};
      }
      :host([aria-checked="true"]:${h.focusVisible}:not([disabled])) .switch {
        outline: solid calc(${R} * 1px) ${u.SystemColors.FieldText};
      }
      :host([disabled]) .checked-indicator {
        background: ${u.SystemColors.GrayText};
      }
      :host([disabled]) .switch {
        background: ${u.SystemColors.Field};
        border-color: ${u.SystemColors.GrayText};
      }
    `),new Qo(zo.css`
        .checked-indicator {
          left: 5px;
          right: calc(((${Ho} / 2) + 1) * 1px);
        }

        :host([aria-checked='true']) .checked-indicator {
          left: calc(((${Ho} / 2) + 1) * 1px);
          right: 5px;
        }
      `,zo.css`
        .checked-indicator {
          right: 5px;
          left: calc(((${Ho} / 2) + 1) * 1px);
        }

        :host([aria-checked='true']) .checked-indicator {
          right: calc(((${Ho} / 2) + 1) * 1px);
          left: 5px;
        }
      `));class ai extends h.Switch{}const ii=ai.compose({baseName:"switch",baseClass:h.Switch,template:h.switchTemplate,styles:ri,switch:'\n        <span class="checked-indicator" part="checked-indicator"></span>\n    '}),li=(e,t)=>zo.css`
  ${(0,h.display)("block")} :host {
    box-sizing: border-box;
    font-size: ${I};
    line-height: ${N};
    padding: 0 calc((6 + (${B} * 2 * ${z})) * 1px);
  }
`;class si extends h.TabPanel{}const ni=si.compose({baseName:"tab-panel",baseClass:h.TabPanel,template:h.tabPanelTemplate,styles:li}),ci=(e,t)=>zo.css`
    ${(0,h.display)("inline-flex")} :host {
      box-sizing: border-box;
      font-family: ${S};
      font-size: ${I};
      line-height: ${N};
      height: calc(${Ho} * 1px);
      padding: calc(${B} * 5px) calc(${B} * 4px);
      color: ${Gt};
      fill: currentcolor;
      border-radius: 0 0 calc(${T} * 1px)
        calc(${T} * 1px);
      border: calc(${O} * 1px) solid transparent;
      align-items: center;
      justify-content: center;
      grid-row: 2;
      cursor: pointer;
    }

    :host(:hover) {
      color: ${Wt};
      fill: currentcolor;
    }

    :host(:active) {
      color: ${Wt};
      fill: currentcolor;
    }

    :host([disabled]) {
      cursor: ${h.disabledCursor};
      opacity: ${L};
    }

    :host([disabled]:hover) {
      color: ${Gt};
      background: ${Dt};
    }

    :host([aria-selected='true']) {
      background: ${ft};
      color: ${Wt};
      fill: currentcolor;
    }

    :host([aria-selected='true']:hover) {
      background: ${vt};
      color: ${Wt};
      fill: currentcolor;
    }

    :host([aria-selected='true']:active) {
      background: ${$t};
      color: ${Wt};
      fill: currentcolor;
    }

    :host(:${h.focusVisible}) {
      outline: none;
      border-color: ${Qe};
      box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
        ${Qe};
    }

    :host(:focus) {
      outline: none;
    }

    :host(.vertical) {
      justify-content: end;
      grid-column: 2;
      border-bottom-left-radius: 0;
      border-top-right-radius: calc(${T} * 1px);
    }

    :host(.vertical[aria-selected='true']) {
      z-index: 2;
    }

    :host(.vertical:hover) {
      color: ${Wt};
    }

    :host(.vertical:active) {
      color: ${Wt};
    }

    :host(.vertical:hover[aria-selected='true']) {
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        forced-color-adjust: none;
        border-color: transparent;
        color: ${u.SystemColors.ButtonText};
        fill: currentcolor;
      }
      :host(:hover),
      :host(.vertical:hover),
      :host([aria-selected='true']:hover) {
        background: ${u.SystemColors.Highlight};
        color: ${u.SystemColors.HighlightText};
        fill: currentcolor;
      }
      :host([aria-selected='true']) {
        background: ${u.SystemColors.HighlightText};
        color: ${u.SystemColors.Highlight};
        fill: currentcolor;
      }
      :host(:${h.focusVisible}) {
        border-color: ${u.SystemColors.ButtonText};
        box-shadow: none;
      }
      :host([disabled]),
      :host([disabled]:hover) {
        opacity: 1;
        color: ${u.SystemColors.GrayText};
        background: ${u.SystemColors.ButtonFace};
      }
    `));class di extends h.Tab{}const hi=di.compose({baseName:"tab",baseClass:h.Tab,template:h.tabTemplate,styles:ci}),ui=(e,t)=>zo.css`
    ${(0,h.display)("grid")} :host {
      box-sizing: border-box;
      font-family: ${S};
      font-size: ${I};
      line-height: ${N};
      color: ${Wt};
      grid-template-columns: auto 1fr auto;
      grid-template-rows: auto 1fr;
    }

    .tablist {
      display: grid;
      grid-template-rows: auto auto;
      grid-template-columns: auto;
      position: relative;
      width: max-content;
      align-self: end;
      padding: calc(${B} * 4px) calc(${B} * 4px) 0;
      box-sizing: border-box;
    }

    .start,
    .end {
      align-self: center;
    }

    .activeIndicator {
      grid-row: 1;
      grid-column: 1;
      width: 100%;
      height: 4px;
      justify-self: center;
      background: ${Ye};
      margin-top: 0;
      border-radius: calc(${T} * 1px)
        calc(${T} * 1px) 0 0;
    }

    .activeIndicatorTransition {
      transition: transform 0.01s ease-in-out;
    }

    .tabpanel {
      grid-row: 2;
      grid-column-start: 1;
      grid-column-end: 4;
      position: relative;
    }

    :host([orientation='vertical']) {
      grid-template-rows: auto 1fr auto;
      grid-template-columns: auto 1fr;
    }

    :host([orientation='vertical']) .tablist {
      grid-row-start: 2;
      grid-row-end: 2;
      display: grid;
      grid-template-rows: auto;
      grid-template-columns: auto 1fr;
      position: relative;
      width: max-content;
      justify-self: end;
      align-self: flex-start;
      width: 100%;
      padding: 0 calc(${B} * 4px)
        calc((${Ho} - ${B}) * 1px) 0;
    }

    :host([orientation='vertical']) .tabpanel {
      grid-column: 2;
      grid-row-start: 1;
      grid-row-end: 4;
    }

    :host([orientation='vertical']) .end {
      grid-row: 3;
    }

    :host([orientation='vertical']) .activeIndicator {
      grid-column: 1;
      grid-row: 1;
      width: 4px;
      height: 100%;
      margin-inline-end: 0px;
      align-self: center;
      background: ${Ye};
      border-radius: calc(${T} * 1px) 0 0
        calc(${T} * 1px);
    }

    :host([orientation='vertical']) .activeIndicatorTransition {
      transition: transform 0.01s ease-in-out;
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      .activeIndicator,
      :host([orientation='vertical']) .activeIndicator {
        forced-color-adjust: none;
        background: ${u.SystemColors.Highlight};
      }
    `));class pi extends h.Tabs{}const gi=pi.compose({baseName:"tabs",baseClass:h.Tabs,template:h.tabsTemplate,styles:ui}),bi=(e,t)=>zo.css`
    ${(0,h.display)("inline-block")} :host {
      font-family: ${S};
      outline: none;
      user-select: none;
    }

    .control {
      box-sizing: border-box;
      position: relative;
      color: ${Wt};
      background: ${kt};
      border-radius: calc(${T} * 1px);
      border: calc(${O} * 1px) solid ${Ht};
      height: calc(${Ho} * 2px);
      font: inherit;
      font-size: ${I};
      line-height: ${N};
      padding: calc(${B} * 2px + 1px);
      width: 100%;
      resize: none;
    }

    :host([aria-invalid='true']) .control {
      border-color: ${ro};
    }

    .control:hover:enabled {
      background: ${wt};
      border-color: ${jt};
    }

    :host([aria-invalid='true']) .control:hover:enabled {
      border-color: ${ao};
    }

    .control:active:enabled {
      background: ${Ct};
      border-color: ${Lt};
    }

    :host([aria-invalid='true']) .control:active:enabled {
      border-color: ${io};
    }

    .control:hover,
    .control:${h.focusVisible},
    .control:disabled,
    .control:active {
      outline: none;
    }

    :host(:focus-within) .control {
      border-color: ${Qe};
      box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
        ${Qe};
    }

    :host([aria-invalid='true']:focus-within) .control {
      border-color: ${lo};
      box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
        ${lo};
    }

    :host([appearance='filled']) .control {
      background: ${ft};
    }

    :host([appearance='filled']:hover:not([disabled])) .control {
      background: ${vt};
    }

    :host([resize='both']) .control {
      resize: both;
    }

    :host([resize='horizontal']) .control {
      resize: horizontal;
    }

    :host([resize='vertical']) .control {
      resize: vertical;
    }

    .label {
      display: block;
      color: ${Wt};
      cursor: pointer;
      font-size: ${I};
      line-height: ${N};
      margin-bottom: 4px;
    }

    .label__hidden {
      display: none;
      visibility: hidden;
    }

    :host([disabled]) .label,
    :host([readonly]) .label,
    :host([readonly]) .control,
    :host([disabled]) .control {
      cursor: ${h.disabledCursor};
    }
    :host([disabled]) {
      opacity: ${L};
    }
    :host([disabled]) .control {
      border-color: ${qt};
    }

    :host([cols]) {
      width: initial;
    }

    :host([rows]) .control {
      height: initial;
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host([disabled]) {
        opacity: 1;
      }

      :host([aria-invalid='true']) .control {
        border-style: dashed;
      }
    `));class mi extends h.TextArea{constructor(){super(...arguments),this.appearance="outline"}}No([zo.attr],mi.prototype,"appearance",void 0);const fi=mi.compose({baseName:"text-area",baseClass:h.TextArea,template:h.textAreaTemplate,styles:bi,shadowOptions:{delegatesFocus:!0}}),vi=(e,t)=>zo.css`
  ${_r}

  .start,
    .end {
    display: flex;
  }
`;class $i extends h.TextField{constructor(){super(...arguments),this.appearance="outline"}}No([zo.attr],$i.prototype,"appearance",void 0);const xi=$i.compose({baseName:"text-field",baseClass:h.TextField,template:h.textFieldTemplate,styles:vi,shadowOptions:{delegatesFocus:!0}});var yi=o(13066);const ki=(e,t)=>zo.css`
    ${(0,h.display)("inline-flex")} :host {
      --toolbar-item-gap: calc(
        (var(--design-unit) + calc(var(--density) + 2)) * 1px
      );
      background-color: ${qe};
      border-radius: calc(${T} * 1px);
      fill: currentcolor;
      padding: var(--toolbar-item-gap);
    }

    :host(${h.focusVisible}) {
      outline: calc(${O} * 1px) solid ${Qe};
    }

    .positioning-region {
      align-items: flex-start;
      display: inline-flex;
      flex-flow: row wrap;
      justify-content: flex-start;
      width: 100%;
      height: 100%;
    }

    :host([orientation='vertical']) .positioning-region {
      flex-direction: column;
    }

    ::slotted(:not([slot])) {
      flex: 0 0 auto;
      margin: 0 var(--toolbar-item-gap);
    }

    :host([orientation='vertical']) ::slotted(:not([slot])) {
      margin: var(--toolbar-item-gap) 0;
    }

    .start,
    .end {
      display: flex;
      margin: auto;
      margin-inline: 0;
    }

    ::slotted(svg) {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: 16px;
      height: 16px;
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host(:${h.focusVisible}) {
        box-shadow: 0 0 0 calc(${R} * 1px)
          ${u.SystemColors.Highlight};
        color: ${u.SystemColors.ButtonText};
        forced-color-adjust: none;
      }
    `)),wi=Object.freeze({[u.ArrowKeys.ArrowUp]:{[u.Orientation.vertical]:-1},[u.ArrowKeys.ArrowDown]:{[u.Orientation.vertical]:1},[u.ArrowKeys.ArrowLeft]:{[u.Orientation.horizontal]:{[u.Direction.ltr]:-1,[u.Direction.rtl]:1}},[u.ArrowKeys.ArrowRight]:{[u.Orientation.horizontal]:{[u.Direction.ltr]:1,[u.Direction.rtl]:-1}}});class Ci extends h.FoundationElement{constructor(){super(...arguments),this._activeIndex=0,this.direction=u.Direction.ltr,this.orientation=u.Orientation.horizontal}get activeIndex(){return zo.Observable.track(this,"activeIndex"),this._activeIndex}set activeIndex(e){this.$fastController.isConnected&&(this._activeIndex=(0,u.limit)(0,this.focusableElements.length-1,e),zo.Observable.notify(this,"activeIndex"))}slottedItemsChanged(){this.$fastController.isConnected&&this.reduceFocusableElements()}mouseDownHandler(e){var t;const o=null===(t=this.focusableElements)||void 0===t?void 0:t.findIndex(t=>t.contains(e.target));return o>-1&&this.activeIndex!==o&&this.setFocusedElement(o),!0}childItemsChanged(e,t){this.$fastController.isConnected&&this.reduceFocusableElements()}connectedCallback(){super.connectedCallback(),this.direction=(0,h.getDirection)(this)}focusinHandler(e){const t=e.relatedTarget;t&&!this.contains(t)&&this.setFocusedElement()}getDirectionalIncrementer(e){var t,o,r,a,i;return null!==(i=null!==(r=null===(o=null===(t=wi[e])||void 0===t?void 0:t[this.orientation])||void 0===o?void 0:o[this.direction])&&void 0!==r?r:null===(a=wi[e])||void 0===a?void 0:a[this.orientation])&&void 0!==i?i:0}keydownHandler(e){const t=e.key;if(!(t in u.ArrowKeys)||e.defaultPrevented||e.shiftKey)return!0;const o=this.getDirectionalIncrementer(t);if(!o)return!e.target.closest("[role=radiogroup]");const r=this.activeIndex+o;return this.focusableElements[r]&&e.preventDefault(),this.setFocusedElement(r),!0}get allSlottedItems(){return[...this.start.assignedElements(),...this.slottedItems,...this.end.assignedElements()]}reduceFocusableElements(){var e;const t=null===(e=this.focusableElements)||void 0===e?void 0:e[this.activeIndex];this.focusableElements=this.allSlottedItems.reduce(Ci.reduceFocusableItems,[]);const o=this.focusableElements.indexOf(t);this.activeIndex=Math.max(0,o),this.setFocusableElements()}setFocusedElement(e=this.activeIndex){this.activeIndex=e,this.setFocusableElements(),this.focusableElements[this.activeIndex]&&this.contains(document.activeElement)&&this.focusableElements[this.activeIndex].focus()}static reduceFocusableItems(e,t){var o,r,a,i;const l="radio"===t.getAttribute("role"),s=null===(r=null===(o=t.$fastController)||void 0===o?void 0:o.definition.shadowOptions)||void 0===r?void 0:r.delegatesFocus,n=Array.from(null!==(i=null===(a=t.shadowRoot)||void 0===a?void 0:a.querySelectorAll("*"))&&void 0!==i?i:[]).some(e=>(0,yi.tp)(e));return t.hasAttribute("disabled")||t.hasAttribute("hidden")||!((0,yi.tp)(t)||l||s||n)?t.childElementCount?e.concat(Array.from(t.children).reduce(Ci.reduceFocusableItems,[])):e:(e.push(t),e)}setFocusableElements(){this.$fastController.isConnected&&this.focusableElements.length>0&&this.focusableElements.forEach((e,t)=>{e.tabIndex=this.activeIndex===t?0:-1})}}No([zo.observable],Ci.prototype,"direction",void 0),No([zo.attr],Ci.prototype,"orientation",void 0),No([zo.observable],Ci.prototype,"slottedItems",void 0),No([zo.observable],Ci.prototype,"slottedLabel",void 0),No([zo.observable],Ci.prototype,"childItems",void 0);class Si{}No([(0,zo.attr)({attribute:"aria-labelledby"})],Si.prototype,"ariaLabelledby",void 0),No([(0,zo.attr)({attribute:"aria-label"})],Si.prototype,"ariaLabel",void 0),(0,h.applyMixins)(Si,h.ARIAGlobalStatesAndProperties),(0,h.applyMixins)(Ci,h.StartEnd,Si);class Fi extends Ci{connectedCallback(){super.connectedCallback();const e=(0,h.composedParent)(this);e&&qe.setValueFor(this,t=>Rt.getValueFor(t).evaluate(t,qe.getValueFor(e)))}}const Di=Fi.compose({baseName:"toolbar",baseClass:Ci,template:h.toolbarTemplate,styles:ki,shadowOptions:{delegatesFocus:!0}}),Vi=(e,t)=>{const o=e.tagFor(h.AnchoredRegion);return zo.css`
    :host {
      contain: size;
      overflow: visible;
      height: 0;
      width: 0;
    }

    .tooltip {
      box-sizing: border-box;
      border-radius: calc(${T} * 1px);
      border: calc(${O} * 1px) solid ${At};
      box-shadow: 0 0 0 1px ${At} inset;
      background: ${ft};
      color: ${Wt};
      padding: 4px;
      height: fit-content;
      width: fit-content;
      font-family: ${S};
      font-size: ${I};
      line-height: ${N};
      white-space: nowrap;
      /* TODO: a mechanism to manage z-index across components
                    https://github.com/microsoft/fast/issues/3813 */
      z-index: 10000;
    }

    ${o} {
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: visible;
      flex-direction: row;
    }

    ${o}.right,
    ${o}.left {
      flex-direction: column;
    }

    ${o}.top .tooltip {
      margin-bottom: 4px;
    }

    ${o}.bottom .tooltip {
      margin-top: 4px;
    }

    ${o}.left .tooltip {
      margin-right: 4px;
    }

    ${o}.right .tooltip {
      margin-left: 4px;
    }

    ${o}.top.left .tooltip,
            ${o}.top.right .tooltip {
      margin-bottom: 0px;
    }

    ${o}.bottom.left .tooltip,
            ${o}.bottom.right .tooltip {
      margin-top: 0px;
    }

    ${o}.top.left .tooltip,
            ${o}.bottom.left .tooltip {
      margin-right: 0px;
    }

    ${o}.top.right .tooltip,
            ${o}.bottom.right .tooltip {
      margin-left: 0px;
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host([disabled]) {
        opacity: 1;
      }
    `))};class Ti extends h.Tooltip{}const zi=Ti.compose({baseName:"tooltip",baseClass:h.Tooltip,template:h.tooltipTemplate,styles:Vi}),Bi=zo.cssPartial`(((${F} + ${z}) * 0.5 + 2) * ${B})`,Hi=zo.css`
  .expand-collapse-glyph {
    transform: rotate(0deg);
  }
  :host(.nested) .expand-collapse-button {
    left: var(
      --expand-collapse-button-nested-width,
      calc(
        (
            ${Bi} +
              ((${F} + ${z}) * 1.25)
          ) * -1px
      )
    );
  }
  :host([selected])::after {
    left: calc(${R} * 1px);
  }
  :host([expanded]) > .positioning-region .expand-collapse-glyph {
    transform: rotate(90deg);
  }
`,ji=zo.css`
  .expand-collapse-glyph {
    transform: rotate(180deg);
  }
  :host(.nested) .expand-collapse-button {
    right: var(
      --expand-collapse-button-nested-width,
      calc(
        (
            ${Bi} +
              ((${F} + ${z}) * 1.25)
          ) * -1px
      )
    );
  }
  :host([selected])::after {
    right: calc(${R} * 1px);
  }
  :host([expanded]) > .positioning-region .expand-collapse-glyph {
    transform: rotate(90deg);
  }
`,Li=h.DesignToken.create("tree-item-expand-collapse-hover").withDefault(e=>{const t=Ft.getValueFor(e);return t.evaluate(e,t.evaluate(e).hover).hover}),Oi=h.DesignToken.create("tree-item-expand-collapse-selected-hover").withDefault(e=>{const t=mt.getValueFor(e);return Ft.getValueFor(e).evaluate(e,t.evaluate(e).rest).hover}),Ri=(e,t)=>zo.css`
    /**
     * This animation exists because when tree item children are conditionally loaded
     * there is a visual bug where the DOM exists but styles have not yet been applied (essentially FOUC).
     * This subtle animation provides a ever so slight timing adjustment for loading that solves the issue.
     */
    @keyframes treeItemLoading {
      0% {
        opacity: 0;
      }
      100% {
        opacity: 1;
      }
    }

    ${(0,h.display)("block")} :host {
      contain: content;
      position: relative;
      outline: none;
      color: ${Wt};
      background: ${Dt};
      cursor: pointer;
      font-family: ${S};
      --tree-item-nested-width: 0;
    }

    :host(:focus) > .positioning-region {
      outline: none;
    }

    :host(:focus) .content-region {
      outline: none;
    }

    :host(:${h.focusVisible}) .positioning-region {
      border-color: ${Qe};
      box-shadow: 0 0 0 calc((${R} - ${O}) * 1px)
        ${Qe} inset;
      color: ${Wt};
    }

    .positioning-region {
      display: flex;
      position: relative;
      box-sizing: border-box;
      background: ${Dt};
      border: transparent calc(${O} * 1px) solid;
      border-radius: calc(${T} * 1px);
      height: calc((${Ho} + 1) * 1px);
    }

    .positioning-region::before {
      content: '';
      display: block;
      width: var(--tree-item-nested-width);
      flex-shrink: 0;
    }

    :host(:not([disabled])) .positioning-region:hover {
      background: ${Vt};
    }

    :host(:not([disabled])) .positioning-region:active {
      background: ${Tt};
    }

    .content-region {
      display: inline-flex;
      align-items: center;
      white-space: nowrap;
      width: 100%;
      min-width: 0;
      height: calc(${Ho} * 1px);
      margin-inline-start: calc(${B} * 2px + 8px);
      font-size: ${I};
      line-height: ${N};
      font-weight: 400;
    }

    .items {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      font-size: calc(1em + (${B} + 16) * 1px);
    }

    .expand-collapse-button {
      background: none;
      border: none;
      outline: none;
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: calc(${Bi} * 1px);
      height: calc(${Bi} * 1px);
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      margin-left: 6px;
      margin-right: 6px;
    }

    .expand-collapse-glyph {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: calc((16 + ${z}) * 1px);
      height: calc((16 + ${z}) * 1px);
      transition: transform 0.1s linear;

      pointer-events: none;
      fill: currentcolor;
    }

    .start,
    .end {
      display: flex;
      fill: currentcolor;
    }

    ::slotted(svg) {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: 16px;
      height: 16px;

      /* Something like that would do if the typography is adaptive
      font-size: inherit;
      width: ${G};
      height: ${G};
      */
    }

    .start {
      /* TODO: horizontalSpacing https://github.com/microsoft/fast/issues/2766 */
      margin-inline-end: calc(${B} * 2px + 2px);
    }

    .end {
      /* TODO: horizontalSpacing https://github.com/microsoft/fast/issues/2766 */
      margin-inline-start: calc(${B} * 2px + 2px);
    }

    :host([expanded]) > .items {
      animation: treeItemLoading ease-in 10ms;
      animation-iteration-count: 1;
      animation-fill-mode: forwards;
    }

    :host([disabled]) .content-region {
      opacity: ${L};
      cursor: ${h.disabledCursor};
    }

    :host(.nested) .content-region {
      position: relative;
      /* Add left margin to collapse button size */
      margin-inline-start: calc(
        (
            ${Bi} +
              ((${F} + ${z}) * 1.25)
          ) * 1px
      );
    }

    :host(.nested) .expand-collapse-button {
      position: absolute;
    }

    :host(.nested:not([disabled])) .expand-collapse-button:hover {
      background: ${Li};
    }

    :host([selected]) .positioning-region {
      background: ${ft};
    }

    :host([selected]:not([disabled])) .positioning-region:hover {
      background: ${vt};
    }

    :host([selected]:not([disabled])) .positioning-region:active {
      background: ${$t};
    }

    :host([selected]:not([disabled])) .expand-collapse-button:hover {
      background: ${Oi};
    }

    :host([selected])::after {
      /* The background needs to be calculated based on the selected background state
         for this control. We currently have no way of changing that, so setting to
         accent-foreground-rest for the time being */
      background: ${ut};
      border-radius: calc(${T} * 1px);
      content: '';
      display: block;
      position: absolute;
      top: calc((${Ho} / 4) * 1px);
      width: 3px;
      height: calc((${Ho} / 2) * 1px);
    }

    ::slotted(${e.tagFor(h.TreeItem)}) {
      --tree-item-nested-width: 1em;
      --expand-collapse-button-nested-width: calc(
        (
            ${Bi} +
              ((${F} + ${z}) * 1.25)
          ) * -1px
      );
    }
  `.withBehaviors(new Qo(Hi,ji),(0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        forced-color-adjust: none;
        border-color: transparent;
        background: ${u.SystemColors.Field};
        color: ${u.SystemColors.FieldText};
      }
      :host .content-region .expand-collapse-glyph {
        fill: ${u.SystemColors.FieldText};
      }
      :host .positioning-region:hover,
      :host([selected]) .positioning-region {
        background: ${u.SystemColors.Highlight};
      }
      :host .positioning-region:hover .content-region,
      :host([selected]) .positioning-region .content-region {
        color: ${u.SystemColors.HighlightText};
      }
      :host .positioning-region:hover .content-region .expand-collapse-glyph,
      :host .positioning-region:hover .content-region .start,
      :host .positioning-region:hover .content-region .end,
      :host([selected]) .content-region .expand-collapse-glyph,
      :host([selected]) .content-region .start,
      :host([selected]) .content-region .end {
        fill: ${u.SystemColors.HighlightText};
      }
      :host([selected])::after {
        background: ${u.SystemColors.Field};
      }
      :host(:${h.focusVisible}) .positioning-region {
        border-color: ${u.SystemColors.FieldText};
        box-shadow: 0 0 0 2px inset ${u.SystemColors.Field};
        color: ${u.SystemColors.FieldText};
      }
      :host([disabled]) .content-region,
      :host([disabled]) .positioning-region:hover .content-region {
        opacity: 1;
        color: ${u.SystemColors.GrayText};
      }
      :host([disabled]) .content-region .expand-collapse-glyph,
      :host([disabled]) .content-region .start,
      :host([disabled]) .content-region .end,
      :host([disabled])
        .positioning-region:hover
        .content-region
        .expand-collapse-glyph,
      :host([disabled]) .positioning-region:hover .content-region .start,
      :host([disabled]) .positioning-region:hover .content-region .end {
        fill: ${u.SystemColors.GrayText};
      }
      :host([disabled]) .positioning-region:hover {
        background: ${u.SystemColors.Field};
      }
      .expand-collapse-glyph,
      .start,
      .end {
        fill: ${u.SystemColors.FieldText};
      }
      :host(.nested) .expand-collapse-button:hover {
        background: ${u.SystemColors.Field};
      }
      :host(.nested) .expand-collapse-button:hover .expand-collapse-glyph {
        fill: ${u.SystemColors.FieldText};
      }
    `));class Ii extends h.TreeItem{}const Ni=Ii.compose({baseName:"tree-item",baseClass:h.TreeItem,template:h.treeItemTemplate,styles:Ri,expandCollapseGlyph:'\n        <svg\n            viewBox="0 0 16 16"\n            xmlns="http://www.w3.org/2000/svg"\n            class="expand-collapse-glyph"\n        >\n            <path\n                d="M5.00001 12.3263C5.00124 12.5147 5.05566 12.699 5.15699 12.8578C5.25831 13.0167 5.40243 13.1437 5.57273 13.2242C5.74304 13.3047 5.9326 13.3354 6.11959 13.3128C6.30659 13.2902 6.4834 13.2152 6.62967 13.0965L10.8988 8.83532C11.0739 8.69473 11.2153 8.51658 11.3124 8.31402C11.4096 8.11146 11.46 7.88966 11.46 7.66499C11.46 7.44033 11.4096 7.21853 11.3124 7.01597C11.2153 6.81341 11.0739 6.63526 10.8988 6.49467L6.62967 2.22347C6.48274 2.10422 6.30501 2.02912 6.11712 2.00691C5.92923 1.9847 5.73889 2.01628 5.56823 2.09799C5.39757 2.17969 5.25358 2.30817 5.153 2.46849C5.05241 2.62882 4.99936 2.8144 5.00001 3.00369V12.3263Z"\n            />\n        </svg>\n    '}),Ai=(e,t)=>zo.css`
  ${(0,h.display)("flex")} :host {
    flex-direction: column;
    align-items: stretch;
    min-width: fit-content;
    font-size: 0;
  }

  :host:focus-visible {
    outline: none;
  }
`;class Pi extends h.TreeView{handleClick(e){if(e.defaultPrevented)return;if(!(e.target instanceof Element))return!0;let t=e.target;for(;t&&!(0,h.isTreeItemElement)(t);)t=t.parentElement,t===this&&(t=null);t&&!t.disabled&&(t.selected=!0)}}const Ei=Pi.compose({baseName:"tree-view",baseClass:h.TreeView,template:h.treeViewTemplate,styles:Ai}),Mi=(e,t)=>zo.css`
  .region {
    z-index: 1000;
    overflow: hidden;
    display: flex;
    font-family: ${S};
    font-size: ${I};
  }

  .loaded {
    opacity: 1;
    pointer-events: none;
  }

  .loading-display,
  .no-options-display {
    background: ${qe};
    width: 100%;
    min-height: calc(${Ho} * 1px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-items: center;
    padding: calc(${B} * 1px);
  }

  .loading-progress {
    width: 42px;
    height: 42px;
  }

  .bottom {
    flex-direction: column;
  }

  .top {
    flex-direction: column-reverse;
  }
`,Gi=(e,t)=>zo.css`
    :host {
      background: ${qe};
      --elevation: 11;
      /* TODO: a mechanism to manage z-index across components
            https://github.com/microsoft/fast/issues/3813 */
      z-index: 1000;
      display: flex;
      width: 100%;
      max-height: 100%;
      min-height: 58px;
      box-sizing: border-box;
      flex-direction: column;
      overflow-y: auto;
      overflow-x: hidden;
      pointer-events: auto;
      border-radius: calc(${T} * 1px);
      padding: calc(${B} * 1px) 0;
      border: calc(${O} * 1px) solid transparent;
      ${fr}
    }

    .suggestions-available-alert {
      height: 0;
      opacity: 0;
      overflow: hidden;
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        background: ${u.SystemColors.Canvas};
        border-color: ${u.SystemColors.CanvasText};
      }
    `)),_i=(e,t)=>zo.css`
    :host {
      display: flex;
      align-items: center;
      justify-items: center;
      font-family: ${S};
      border-radius: calc(${T} * 1px);
      border: calc(${R} * 1px) solid transparent;
      box-sizing: border-box;
      background: ${Dt};
      color: ${Wt};
      cursor: pointer;
      fill: currentcolor;
      font-size: ${I};
      min-height: calc(${Ho} * 1px);
      line-height: ${N};
      margin: 0 calc(${B} * 1px);
      outline: none;
      overflow: hidden;
      padding: 0 calc(${B} * 2.25px);
      user-select: none;
      white-space: nowrap;
    }

    :host(:${h.focusVisible}[role="listitem"]) {
      border-color: ${At};
      background: ${zt};
    }

    :host(:hover) {
      background: ${Vt};
    }

    :host(:active) {
      background: ${Tt};
    }

    :host([aria-selected='true']) {
      background: ${Ye};
      color: ${ot};
    }

    :host([aria-selected='true']:hover) {
      background: ${Ze};
      color: ${rt};
    }

    :host([aria-selected='true']:active) {
      background: ${Je};
      color: ${at};
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        border-color: transparent;
        forced-color-adjust: none;
        color: ${u.SystemColors.ButtonText};
        fill: currentcolor;
      }

      :host(:not([aria-selected='true']):hover),
      :host([aria-selected='true']) {
        background: ${u.SystemColors.Highlight};
        color: ${u.SystemColors.HighlightText};
      }

      :host([disabled]),
      :host([disabled]:not([aria-selected='true']):hover) {
        background: ${u.SystemColors.Canvas};
        color: ${u.SystemColors.GrayText};
        fill: currentcolor;
        opacity: 1;
      }
    `)),Wi=(e,t)=>zo.css`
    :host {
      display: flex;
      align-items: center;
      justify-items: center;
      font-family: ${S};
      border-radius: calc(${T} * 1px);
      border: calc(${R} * 1px) solid transparent;
      box-sizing: border-box;
      background: ${Dt};
      color: ${Wt};
      cursor: pointer;
      fill: currentcolor;
      font-size: ${I};
      height: calc(${Ho} * 1px);
      line-height: ${N};
      outline: none;
      overflow: hidden;
      padding: 0 calc(${B} * 2.25px);
      user-select: none;
      white-space: nowrap;
    }

    :host(:hover) {
      background: ${Vt};
    }

    :host(:active) {
      background: ${Tt};
    }

    :host(:${h.focusVisible}) {
      background: ${zt};
      border-color: ${At};
    }

    :host([aria-selected='true']) {
      background: ${Ye};
      color: ${at};
    }
  `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      :host {
        border-color: transparent;
        forced-color-adjust: none;
        color: ${u.SystemColors.ButtonText};
        fill: currentcolor;
      }

      :host(:not([aria-selected='true']):hover),
      :host([aria-selected='true']) {
        background: ${u.SystemColors.Highlight};
        color: ${u.SystemColors.HighlightText};
      }

      :host([disabled]),
      :host([disabled]:not([aria-selected='true']):hover) {
        background: ${u.SystemColors.Canvas};
        color: ${u.SystemColors.GrayText};
        fill: currentcolor;
        opacity: 1;
      }
    `));class Ui extends h.Picker{}const qi=Ui.compose({baseName:"draft-picker",baseClass:h.Picker,template:h.pickerTemplate,styles:Mi,shadowOptions:{}});class Xi extends h.PickerMenu{connectedCallback(){qe.setValueFor(this,Ne),super.connectedCallback()}}const Ki=Xi.compose({baseName:"draft-picker-menu",baseClass:h.PickerMenu,template:h.pickerMenuTemplate,styles:Gi});class Yi extends h.PickerMenuOption{}const Zi=Yi.compose({baseName:"draft-picker-menu-option",baseClass:h.PickerMenuOption,template:h.pickerMenuOptionTemplate,styles:_i});class Ji extends h.PickerList{}const Qi=Ji.compose({baseName:"draft-picker-list",baseClass:h.PickerList,template:h.pickerListTemplate,styles:(e,t)=>zo.css`
        :host {
            display: flex;
            flex-direction: row;
            column-gap: calc(${B} * 1px);
            row-gap: calc(${B} * 1px);
            flex-wrap: wrap;
        }

        ::slotted([role="combobox"]) {
            min-width: 260px;
            width: auto;
            box-sizing: border-box;
            color: ${Wt};
            background: ${kt};
            border-radius: calc(${T} * 1px);
            border: calc(${O} * 1px) solid ${Ye};
            height: calc(${Ho} * 1px);
            font-family: ${S};
            outline: none;
            user-select: none;
            font-size: ${I};
            line-height: ${N};
            padding: 0 calc(${B} * 2px + 1px);
        }

        ::slotted([role="combobox"]:active) { {
            background: ${wt};
            border-color: ${Je};
        }

        ::slotted([role="combobox"]:focus-within) {
            border-color: ${At};
            box-shadow: 0 0 0 1px ${At} inset;
        }
    `.withBehaviors((0,h.forcedColorsStylesheetBehavior)(zo.css`
      ::slotted([role='combobox']:active) {
        background: ${u.SystemColors.Field};
        border-color: ${u.SystemColors.Highlight};
      }
      ::slotted([role='combobox']:focus-within) {
        border-color: ${u.SystemColors.Highlight};
        box-shadow: 0 0 0 1px ${u.SystemColors.Highlight} inset;
      }
      ::slotted(input:placeholder) {
        color: ${u.SystemColors.GrayText};
      }
    `))});class el extends h.PickerListItem{}const tl=el.compose({baseName:"draft-picker-list-item",baseClass:h.PickerListItem,template:h.pickerListItemTemplate,styles:Wi}),ol={jpAccordion:Io,jpAccordionItem:Oo,jpAnchor:Ko,jpAnchoredRegion:Jo,jpAvatar:ar,jpBadge:sr,jpBreadcrumb:dr,jpBreadcrumbItem:pr,jpButton:mr,jpCard:xr,jpCheckbox:Cr,jpCombobox:Tr,jpDataGrid:Nr,jpDataGridCell:Lr,jpDataGridRow:Rr,jpDateField:qr,jpDesignSystemProvider:ea,jpDialog:ra,jpDisclosure:la,jpDivider:ca,jpListbox:ha,jpMenu:ga,jpMenuItem:fa,jpNumberField:xa,jpOption:wa,jpPicker:qi,jpPickerList:Qi,jpPickerListItem:tl,jpPickerMenu:Ki,jpPickerMenuOption:Zi,jpProgress:Fa,jpProgressRing:Ta,jpRadio:ja,jpRadioGroup:Ra,jpSearch:Ea,jpSelect:Ga,jpSkeleton:Ua,jpSlider:Za,jpSliderLabel:oi,jpSwitch:ii,jpTab:hi,jpTabPanel:ni,jpTabs:gi,jpTextArea:fi,jpTextField:xi,jpToolbar:Di,jpTooltip:zi,jpTreeItem:Ni,jpTreeView:Ei,register(e,...t){if(e)for(const o in this)"register"!==o&&this[o]().register(e,...t)}};function rl(e){return h.DesignSystem.getOrCreate(e).withPrefix("jp")}}}]);