import{r as e,t}from"./jsx-runtime-DAs1UGHr.js";import{t as n}from"./react-DxF41JXl.js";import{n as r}from"./use-runtime-config-D_-Z8FUB.js";var i=()=>({isAuthenticated:r().authenticated});function a(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function o(e){if(Array.isArray(e))return e}function s(e){if(Array.isArray(e))return a(e)}function c(e,t){if(!(e instanceof t))throw TypeError(`Cannot call a class as a function`)}function l(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,`value`in r&&(r.writable=!0),Object.defineProperty(e,ee(r.key),r)}}function u(e,t,n){return t&&l(e.prototype,t),n&&l(e,n),Object.defineProperty(e,`prototype`,{writable:!1}),e}function d(e,t){var n=typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(!n){if(Array.isArray(e)||(n=ne(e))||t&&e&&typeof e.length==`number`){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var a,o=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||n.return==null||n.return()}finally{if(s)throw a}}}}function f(e,t,n){return(t=ee(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function p(e){if(typeof Symbol<`u`&&e[Symbol.iterator]!=null||e[`@@iterator`]!=null)return Array.from(e)}function m(e,t){var n=e==null?null:typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(n!=null){var r,i,a,o,s=[],c=!0,l=!1;try{if(a=(n=n.call(e)).next,t===0){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=a.call(n)).done)&&(s.push(r.value),s.length!==t);c=!0);}catch(e){l=!0,i=e}finally{try{if(!c&&n.return!=null&&(o=n.return(),Object(o)!==o))return}finally{if(l)throw i}}return s}}function h(){throw TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function g(){throw TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function _(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function v(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?_(Object(n),!0).forEach(function(t){f(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):_(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function y(e,t){return o(e)||m(e,t)||ne(e,t)||h()}function b(e){return s(e)||p(e)||ne(e)||g()}function x(e,t){if(typeof e!=`object`||!e)return e;var n=e[Symbol.toPrimitive];if(n!==void 0){var r=n.call(e,t||`default`);if(typeof r!=`object`)return r;throw TypeError(`@@toPrimitive must return a primitive value.`)}return(t===`string`?String:Number)(e)}function ee(e){var t=x(e,`string`);return typeof t==`symbol`?t:t+``}function te(e){"@babel/helpers - typeof";return te=typeof Symbol==`function`&&typeof Symbol.iterator==`symbol`?function(e){return typeof e}:function(e){return e&&typeof Symbol==`function`&&e.constructor===Symbol&&e!==Symbol.prototype?`symbol`:typeof e},te(e)}function ne(e,t){if(e){if(typeof e==`string`)return a(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?a(e,t):void 0}}var re=function(){},ie={},ae={},oe=null,se={mark:re,measure:re};try{typeof window<`u`&&(ie=window),typeof document<`u`&&(ae=document),typeof MutationObserver<`u`&&(oe=MutationObserver),typeof performance<`u`&&(se=performance)}catch{}var ce=(ie.navigator||{}).userAgent,le=ce===void 0?``:ce,S=ie,C=ae,ue=oe,de=se;S.document;var w=!!C.documentElement&&!!C.head&&typeof C.addEventListener==`function`&&typeof C.createElement==`function`,fe=~le.indexOf(`MSIE`)||~le.indexOf(`Trident/`),pe,me=/fa(k|kd|s|r|l|t|d|dr|dl|dt|b|slr|slpr|wsb|tl|ns|nds|es|jr|jfr|jdr|usb|ufsb|udsb|cr|ss|sr|sl|st|sds|sdr|sdl|sdt)?[\-\ ]/,he=/Font ?Awesome ?([567 ]*)(Solid|Regular|Light|Thin|Duotone|Brands|Free|Pro|Sharp Duotone|Sharp|Kit|Notdog Duo|Notdog|Chisel|Etch|Thumbprint|Jelly Fill|Jelly Duo|Jelly|Utility|Utility Fill|Utility Duo|Slab Press|Slab|Whiteboard)?.*/i,ge={classic:{fa:`solid`,fas:`solid`,"fa-solid":`solid`,far:`regular`,"fa-regular":`regular`,fal:`light`,"fa-light":`light`,fat:`thin`,"fa-thin":`thin`,fab:`brands`,"fa-brands":`brands`},duotone:{fa:`solid`,fad:`solid`,"fa-solid":`solid`,"fa-duotone":`solid`,fadr:`regular`,"fa-regular":`regular`,fadl:`light`,"fa-light":`light`,fadt:`thin`,"fa-thin":`thin`},sharp:{fa:`solid`,fass:`solid`,"fa-solid":`solid`,fasr:`regular`,"fa-regular":`regular`,fasl:`light`,"fa-light":`light`,fast:`thin`,"fa-thin":`thin`},"sharp-duotone":{fa:`solid`,fasds:`solid`,"fa-solid":`solid`,fasdr:`regular`,"fa-regular":`regular`,fasdl:`light`,"fa-light":`light`,fasdt:`thin`,"fa-thin":`thin`},slab:{"fa-regular":`regular`,faslr:`regular`},"slab-press":{"fa-regular":`regular`,faslpr:`regular`},thumbprint:{"fa-light":`light`,fatl:`light`},whiteboard:{"fa-semibold":`semibold`,fawsb:`semibold`},notdog:{"fa-solid":`solid`,fans:`solid`},"notdog-duo":{"fa-solid":`solid`,fands:`solid`},etch:{"fa-solid":`solid`,faes:`solid`},jelly:{"fa-regular":`regular`,fajr:`regular`},"jelly-fill":{"fa-regular":`regular`,fajfr:`regular`},"jelly-duo":{"fa-regular":`regular`,fajdr:`regular`},chisel:{"fa-regular":`regular`,facr:`regular`},utility:{"fa-semibold":`semibold`,fausb:`semibold`},"utility-duo":{"fa-semibold":`semibold`,faudsb:`semibold`},"utility-fill":{"fa-semibold":`semibold`,faufsb:`semibold`}},_e={GROUP:`duotone-group`,SWAP_OPACITY:`swap-opacity`,PRIMARY:`primary`,SECONDARY:`secondary`},ve=[`fa-classic`,`fa-duotone`,`fa-sharp`,`fa-sharp-duotone`,`fa-thumbprint`,`fa-whiteboard`,`fa-notdog`,`fa-notdog-duo`,`fa-chisel`,`fa-etch`,`fa-jelly`,`fa-jelly-fill`,`fa-jelly-duo`,`fa-slab`,`fa-slab-press`,`fa-utility`,`fa-utility-duo`,`fa-utility-fill`],T=`classic`,E=`duotone`,ye=`sharp`,be=`sharp-duotone`,xe=`chisel`,Se=`etch`,Ce=`jelly`,we=`jelly-duo`,Te=`jelly-fill`,Ee=`notdog`,De=`notdog-duo`,Oe=`slab`,ke=`slab-press`,Ae=`thumbprint`,je=`utility`,Me=`utility-duo`,Ne=`utility-fill`,Pe=`whiteboard`,Fe=`Classic`,Ie=`Duotone`,Le=`Sharp`,Re=`Sharp Duotone`,ze=`Chisel`,Be=`Etch`,Ve=`Jelly`,He=`Jelly Duo`,Ue=`Jelly Fill`,We=`Notdog`,Ge=`Notdog Duo`,Ke=`Slab`,qe=`Slab Press`,Je=`Thumbprint`,Ye=`Utility`,Xe=`Utility Duo`,Ze=`Utility Fill`,Qe=`Whiteboard`,$e=[T,E,ye,be,xe,Se,Ce,we,Te,Ee,De,Oe,ke,Ae,je,Me,Ne,Pe];pe={},f(f(f(f(f(f(f(f(f(f(pe,T,Fe),E,Ie),ye,Le),be,Re),xe,ze),Se,Be),Ce,Ve),we,He),Te,Ue),Ee,We),f(f(f(f(f(f(f(f(pe,De,Ge),Oe,Ke),ke,qe),Ae,Je),je,Ye),Me,Xe),Ne,Ze),Pe,Qe);var et={classic:{900:`fas`,400:`far`,normal:`far`,300:`fal`,100:`fat`},duotone:{900:`fad`,400:`fadr`,300:`fadl`,100:`fadt`},sharp:{900:`fass`,400:`fasr`,300:`fasl`,100:`fast`},"sharp-duotone":{900:`fasds`,400:`fasdr`,300:`fasdl`,100:`fasdt`},slab:{400:`faslr`},"slab-press":{400:`faslpr`},whiteboard:{600:`fawsb`},thumbprint:{300:`fatl`},notdog:{900:`fans`},"notdog-duo":{900:`fands`},etch:{900:`faes`},chisel:{400:`facr`},jelly:{400:`fajr`},"jelly-fill":{400:`fajfr`},"jelly-duo":{400:`fajdr`},utility:{600:`fausb`},"utility-duo":{600:`faudsb`},"utility-fill":{600:`faufsb`}},tt={"Font Awesome 7 Free":{900:`fas`,400:`far`},"Font Awesome 7 Pro":{900:`fas`,400:`far`,normal:`far`,300:`fal`,100:`fat`},"Font Awesome 7 Brands":{400:`fab`,normal:`fab`},"Font Awesome 7 Duotone":{900:`fad`,400:`fadr`,normal:`fadr`,300:`fadl`,100:`fadt`},"Font Awesome 7 Sharp":{900:`fass`,400:`fasr`,normal:`fasr`,300:`fasl`,100:`fast`},"Font Awesome 7 Sharp Duotone":{900:`fasds`,400:`fasdr`,normal:`fasdr`,300:`fasdl`,100:`fasdt`},"Font Awesome 7 Jelly":{400:`fajr`,normal:`fajr`},"Font Awesome 7 Jelly Fill":{400:`fajfr`,normal:`fajfr`},"Font Awesome 7 Jelly Duo":{400:`fajdr`,normal:`fajdr`},"Font Awesome 7 Slab":{400:`faslr`,normal:`faslr`},"Font Awesome 7 Slab Press":{400:`faslpr`,normal:`faslpr`},"Font Awesome 7 Thumbprint":{300:`fatl`,normal:`fatl`},"Font Awesome 7 Notdog":{900:`fans`,normal:`fans`},"Font Awesome 7 Notdog Duo":{900:`fands`,normal:`fands`},"Font Awesome 7 Etch":{900:`faes`,normal:`faes`},"Font Awesome 7 Chisel":{400:`facr`,normal:`facr`},"Font Awesome 7 Whiteboard":{600:`fawsb`,normal:`fawsb`},"Font Awesome 7 Utility":{600:`fausb`,normal:`fausb`},"Font Awesome 7 Utility Duo":{600:`faudsb`,normal:`faudsb`},"Font Awesome 7 Utility Fill":{600:`faufsb`,normal:`faufsb`}},nt=new Map([[`classic`,{defaultShortPrefixId:`fas`,defaultStyleId:`solid`,styleIds:[`solid`,`regular`,`light`,`thin`,`brands`],futureStyleIds:[],defaultFontWeight:900}],[`duotone`,{defaultShortPrefixId:`fad`,defaultStyleId:`solid`,styleIds:[`solid`,`regular`,`light`,`thin`],futureStyleIds:[],defaultFontWeight:900}],[`sharp`,{defaultShortPrefixId:`fass`,defaultStyleId:`solid`,styleIds:[`solid`,`regular`,`light`,`thin`],futureStyleIds:[],defaultFontWeight:900}],[`sharp-duotone`,{defaultShortPrefixId:`fasds`,defaultStyleId:`solid`,styleIds:[`solid`,`regular`,`light`,`thin`],futureStyleIds:[],defaultFontWeight:900}],[`chisel`,{defaultShortPrefixId:`facr`,defaultStyleId:`regular`,styleIds:[`regular`],futureStyleIds:[],defaultFontWeight:400}],[`etch`,{defaultShortPrefixId:`faes`,defaultStyleId:`solid`,styleIds:[`solid`],futureStyleIds:[],defaultFontWeight:900}],[`jelly`,{defaultShortPrefixId:`fajr`,defaultStyleId:`regular`,styleIds:[`regular`],futureStyleIds:[],defaultFontWeight:400}],[`jelly-duo`,{defaultShortPrefixId:`fajdr`,defaultStyleId:`regular`,styleIds:[`regular`],futureStyleIds:[],defaultFontWeight:400}],[`jelly-fill`,{defaultShortPrefixId:`fajfr`,defaultStyleId:`regular`,styleIds:[`regular`],futureStyleIds:[],defaultFontWeight:400}],[`notdog`,{defaultShortPrefixId:`fans`,defaultStyleId:`solid`,styleIds:[`solid`],futureStyleIds:[],defaultFontWeight:900}],[`notdog-duo`,{defaultShortPrefixId:`fands`,defaultStyleId:`solid`,styleIds:[`solid`],futureStyleIds:[],defaultFontWeight:900}],[`slab`,{defaultShortPrefixId:`faslr`,defaultStyleId:`regular`,styleIds:[`regular`],futureStyleIds:[],defaultFontWeight:400}],[`slab-press`,{defaultShortPrefixId:`faslpr`,defaultStyleId:`regular`,styleIds:[`regular`],futureStyleIds:[],defaultFontWeight:400}],[`thumbprint`,{defaultShortPrefixId:`fatl`,defaultStyleId:`light`,styleIds:[`light`],futureStyleIds:[],defaultFontWeight:300}],[`utility`,{defaultShortPrefixId:`fausb`,defaultStyleId:`semibold`,styleIds:[`semibold`],futureStyleIds:[],defaultFontWeight:600}],[`utility-duo`,{defaultShortPrefixId:`faudsb`,defaultStyleId:`semibold`,styleIds:[`semibold`],futureStyleIds:[],defaultFontWeight:600}],[`utility-fill`,{defaultShortPrefixId:`faufsb`,defaultStyleId:`semibold`,styleIds:[`semibold`],futureStyleIds:[],defaultFontWeight:600}],[`whiteboard`,{defaultShortPrefixId:`fawsb`,defaultStyleId:`semibold`,styleIds:[`semibold`],futureStyleIds:[],defaultFontWeight:600}]]),rt={chisel:{regular:`facr`},classic:{brands:`fab`,light:`fal`,regular:`far`,solid:`fas`,thin:`fat`},duotone:{light:`fadl`,regular:`fadr`,solid:`fad`,thin:`fadt`},etch:{solid:`faes`},jelly:{regular:`fajr`},"jelly-duo":{regular:`fajdr`},"jelly-fill":{regular:`fajfr`},notdog:{solid:`fans`},"notdog-duo":{solid:`fands`},sharp:{light:`fasl`,regular:`fasr`,solid:`fass`,thin:`fast`},"sharp-duotone":{light:`fasdl`,regular:`fasdr`,solid:`fasds`,thin:`fasdt`},slab:{regular:`faslr`},"slab-press":{regular:`faslpr`},thumbprint:{light:`fatl`},utility:{semibold:`fausb`},"utility-duo":{semibold:`faudsb`},"utility-fill":{semibold:`faufsb`},whiteboard:{semibold:`fawsb`}},it=[`fak`,`fa-kit`,`fakd`,`fa-kit-duotone`],at={kit:{fak:`kit`,"fa-kit":`kit`},"kit-duotone":{fakd:`kit-duotone`,"fa-kit-duotone":`kit-duotone`}},ot=[`kit`];f(f({},`kit`,`Kit`),`kit-duotone`,`Kit Duotone`);var st={kit:{"fa-kit":`fak`},"kit-duotone":{"fa-kit-duotone":`fakd`}},ct={"Font Awesome Kit":{400:`fak`,normal:`fak`},"Font Awesome Kit Duotone":{400:`fakd`,normal:`fakd`}},lt={kit:{fak:`fa-kit`},"kit-duotone":{fakd:`fa-kit-duotone`}},ut={kit:{kit:`fak`},"kit-duotone":{"kit-duotone":`fakd`}},dt,ft={GROUP:`duotone-group`,SWAP_OPACITY:`swap-opacity`,PRIMARY:`primary`,SECONDARY:`secondary`},pt=[`fa-classic`,`fa-duotone`,`fa-sharp`,`fa-sharp-duotone`,`fa-thumbprint`,`fa-whiteboard`,`fa-notdog`,`fa-notdog-duo`,`fa-chisel`,`fa-etch`,`fa-jelly`,`fa-jelly-fill`,`fa-jelly-duo`,`fa-slab`,`fa-slab-press`,`fa-utility`,`fa-utility-duo`,`fa-utility-fill`];dt={},f(f(f(f(f(f(f(f(f(f(dt,`classic`,`Classic`),`duotone`,`Duotone`),`sharp`,`Sharp`),`sharp-duotone`,`Sharp Duotone`),`chisel`,`Chisel`),`etch`,`Etch`),`jelly`,`Jelly`),`jelly-duo`,`Jelly Duo`),`jelly-fill`,`Jelly Fill`),`notdog`,`Notdog`),f(f(f(f(f(f(f(f(dt,`notdog-duo`,`Notdog Duo`),`slab`,`Slab`),`slab-press`,`Slab Press`),`thumbprint`,`Thumbprint`),`utility`,`Utility`),`utility-duo`,`Utility Duo`),`utility-fill`,`Utility Fill`),`whiteboard`,`Whiteboard`),f(f({},`kit`,`Kit`),`kit-duotone`,`Kit Duotone`);var mt={classic:{"fa-brands":`fab`,"fa-duotone":`fad`,"fa-light":`fal`,"fa-regular":`far`,"fa-solid":`fas`,"fa-thin":`fat`},duotone:{"fa-regular":`fadr`,"fa-light":`fadl`,"fa-thin":`fadt`},sharp:{"fa-solid":`fass`,"fa-regular":`fasr`,"fa-light":`fasl`,"fa-thin":`fast`},"sharp-duotone":{"fa-solid":`fasds`,"fa-regular":`fasdr`,"fa-light":`fasdl`,"fa-thin":`fasdt`},slab:{"fa-regular":`faslr`},"slab-press":{"fa-regular":`faslpr`},whiteboard:{"fa-semibold":`fawsb`},thumbprint:{"fa-light":`fatl`},notdog:{"fa-solid":`fans`},"notdog-duo":{"fa-solid":`fands`},etch:{"fa-solid":`faes`},jelly:{"fa-regular":`fajr`},"jelly-fill":{"fa-regular":`fajfr`},"jelly-duo":{"fa-regular":`fajdr`},chisel:{"fa-regular":`facr`},utility:{"fa-semibold":`fausb`},"utility-duo":{"fa-semibold":`faudsb`},"utility-fill":{"fa-semibold":`faufsb`}},ht={classic:[`fas`,`far`,`fal`,`fat`,`fad`],duotone:[`fadr`,`fadl`,`fadt`],sharp:[`fass`,`fasr`,`fasl`,`fast`],"sharp-duotone":[`fasds`,`fasdr`,`fasdl`,`fasdt`],slab:[`faslr`],"slab-press":[`faslpr`],whiteboard:[`fawsb`],thumbprint:[`fatl`],notdog:[`fans`],"notdog-duo":[`fands`],etch:[`faes`],jelly:[`fajr`],"jelly-fill":[`fajfr`],"jelly-duo":[`fajdr`],chisel:[`facr`],utility:[`fausb`],"utility-duo":[`faudsb`],"utility-fill":[`faufsb`]},gt={classic:{fab:`fa-brands`,fad:`fa-duotone`,fal:`fa-light`,far:`fa-regular`,fas:`fa-solid`,fat:`fa-thin`},duotone:{fadr:`fa-regular`,fadl:`fa-light`,fadt:`fa-thin`},sharp:{fass:`fa-solid`,fasr:`fa-regular`,fasl:`fa-light`,fast:`fa-thin`},"sharp-duotone":{fasds:`fa-solid`,fasdr:`fa-regular`,fasdl:`fa-light`,fasdt:`fa-thin`},slab:{faslr:`fa-regular`},"slab-press":{faslpr:`fa-regular`},whiteboard:{fawsb:`fa-semibold`},thumbprint:{fatl:`fa-light`},notdog:{fans:`fa-solid`},"notdog-duo":{fands:`fa-solid`},etch:{faes:`fa-solid`},jelly:{fajr:`fa-regular`},"jelly-fill":{fajfr:`fa-regular`},"jelly-duo":{fajdr:`fa-regular`},chisel:{facr:`fa-regular`},utility:{fausb:`fa-semibold`},"utility-duo":{faudsb:`fa-semibold`},"utility-fill":{faufsb:`fa-semibold`}},_t=`fa.fas.far.fal.fat.fad.fadr.fadl.fadt.fab.fass.fasr.fasl.fast.fasds.fasdr.fasdl.fasdt.faslr.faslpr.fawsb.fatl.fans.fands.faes.fajr.fajfr.fajdr.facr.fausb.faudsb.faufsb`.split(`.`).concat(pt,[`fa-solid`,`fa-regular`,`fa-light`,`fa-thin`,`fa-duotone`,`fa-brands`,`fa-semibold`]),vt=[`solid`,`regular`,`light`,`thin`,`duotone`,`brands`,`semibold`],yt=[1,2,3,4,5,6,7,8,9,10],bt=yt.concat([11,12,13,14,15,16,17,18,19,20]),xt=[].concat(b(Object.keys(ht)),vt,[`aw`,`fw`,`pull-left`,`pull-right`],[`2xs`,`xs`,`sm`,`lg`,`xl`,`2xl`,`beat`,`border`,`fade`,`beat-fade`,`bounce`,`flip-both`,`flip-horizontal`,`flip-vertical`,`flip`,`inverse`,`layers`,`layers-bottom-left`,`layers-bottom-right`,`layers-counter`,`layers-text`,`layers-top-left`,`layers-top-right`,`li`,`pull-end`,`pull-start`,`pulse`,`rotate-180`,`rotate-270`,`rotate-90`,`rotate-by`,`shake`,`spin-pulse`,`spin-reverse`,`spin`,`stack-1x`,`stack-2x`,`stack`,`ul`,`width-auto`,`width-fixed`,ft.GROUP,ft.SWAP_OPACITY,ft.PRIMARY,ft.SECONDARY],yt.map(function(e){return`${e}x`}),bt.map(function(e){return`w-${e}`})),St={"Font Awesome 5 Free":{900:`fas`,400:`far`},"Font Awesome 5 Pro":{900:`fas`,400:`far`,normal:`far`,300:`fal`},"Font Awesome 5 Brands":{400:`fab`,normal:`fab`},"Font Awesome 5 Duotone":{900:`fad`}},D=`___FONT_AWESOME___`,Ct=16,wt=`fa`,Tt=`svg-inline--fa`,O=`data-fa-i2svg`,Et=`data-fa-pseudo-element`,Dt=`data-fa-pseudo-element-pending`,Ot=`data-prefix`,kt=`data-icon`,At=`fontawesome-i2svg`,jt=`async`,Mt=[`HTML`,`HEAD`,`STYLE`,`SCRIPT`],Nt=[`::before`,`::after`,`:before`,`:after`],Pt=function(){try{return!0}catch{return!1}}();function Ft(e){return new Proxy(e,{get:function(e,t){return t in e?e[t]:e[T]}})}var It=v({},ge);It[T]=v(v(v(v({},{"fa-duotone":`duotone`}),ge[T]),at.kit),at[`kit-duotone`]);var Lt=Ft(It),Rt=v({},rt);Rt[T]=v(v(v(v({},{duotone:`fad`}),Rt[T]),ut.kit),ut[`kit-duotone`]);var zt=Ft(Rt),Bt=v({},gt);Bt[T]=v(v({},Bt[T]),lt.kit);var Vt=Ft(Bt),Ht=v({},mt);Ht[T]=v(v({},Ht[T]),st.kit),Ft(Ht);var Ut=me,Wt=`fa-layers-text`,Gt=he;Ft(v({},et));var Kt=[`class`,`data-prefix`,`data-icon`,`data-fa-transform`,`data-fa-mask`],qt=_e,Jt=[].concat(b(ot),b(xt)),k=S.FontAwesomeConfig||{};function Yt(e){var t=C.querySelector(`script[`+e+`]`);if(t)return t.getAttribute(e)}function Xt(e){return e===``?!0:e===`false`?!1:e===`true`?!0:e}C&&typeof C.querySelector==`function`&&[[`data-family-prefix`,`familyPrefix`],[`data-css-prefix`,`cssPrefix`],[`data-family-default`,`familyDefault`],[`data-style-default`,`styleDefault`],[`data-replacement-class`,`replacementClass`],[`data-auto-replace-svg`,`autoReplaceSvg`],[`data-auto-add-css`,`autoAddCss`],[`data-search-pseudo-elements`,`searchPseudoElements`],[`data-search-pseudo-elements-warnings`,`searchPseudoElementsWarnings`],[`data-search-pseudo-elements-full-scan`,`searchPseudoElementsFullScan`],[`data-observe-mutations`,`observeMutations`],[`data-mutate-approach`,`mutateApproach`],[`data-keep-original-source`,`keepOriginalSource`],[`data-measure-performance`,`measurePerformance`],[`data-show-missing-icons`,`showMissingIcons`]].forEach(function(e){var t=y(e,2),n=t[0],r=t[1],i=Xt(Yt(n));i!=null&&(k[r]=i)});var Zt={styleDefault:`solid`,familyDefault:T,cssPrefix:wt,replacementClass:Tt,autoReplaceSvg:!0,autoAddCss:!0,searchPseudoElements:!1,searchPseudoElementsWarnings:!0,searchPseudoElementsFullScan:!1,observeMutations:!0,mutateApproach:`async`,keepOriginalSource:!0,measurePerformance:!1,showMissingIcons:!0};k.familyPrefix&&(k.cssPrefix=k.familyPrefix);var A=v(v({},Zt),k);A.autoReplaceSvg||(A.observeMutations=!1);var j={};Object.keys(Zt).forEach(function(e){Object.defineProperty(j,e,{enumerable:!0,set:function(t){A[e]=t,M.forEach(function(e){return e(j)})},get:function(){return A[e]}})}),Object.defineProperty(j,`familyPrefix`,{enumerable:!0,set:function(e){A.cssPrefix=e,M.forEach(function(e){return e(j)})},get:function(){return A.cssPrefix}}),S.FontAwesomeConfig=j;var M=[];function Qt(e){return M.push(e),function(){M.splice(M.indexOf(e),1)}}var N=Ct,P={size:16,x:0,y:0,rotate:0,flipX:!1,flipY:!1};function $t(e){if(!(!e||!w)){var t=C.createElement(`style`);t.setAttribute(`type`,`text/css`),t.innerHTML=e;for(var n=C.head.childNodes,r=null,i=n.length-1;i>-1;i--){var a=n[i],o=(a.tagName||``).toUpperCase();[`STYLE`,`LINK`].indexOf(o)>-1&&(r=a)}return C.head.insertBefore(t,r),e}}var en=`0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`;function tn(){for(var e=12,t=``;e-- >0;)t+=en[Math.random()*62|0];return t}function F(e){for(var t=[],n=(e||[]).length>>>0;n--;)t[n]=e[n];return t}function nn(e){return e.classList?F(e.classList):(e.getAttribute(`class`)||``).split(` `).filter(function(e){return e})}function rn(e){return`${e}`.replace(/&/g,`&amp;`).replace(/"/g,`&quot;`).replace(/'/g,`&#39;`).replace(/</g,`&lt;`).replace(/>/g,`&gt;`)}function an(e){return Object.keys(e||{}).reduce(function(t,n){return t+`${n}="${rn(e[n])}" `},``).trim()}function on(e){return Object.keys(e||{}).reduce(function(t,n){return t+`${n}: ${e[n].trim()};`},``)}function sn(e){return e.size!==P.size||e.x!==P.x||e.y!==P.y||e.rotate!==P.rotate||e.flipX||e.flipY}function cn(e){var t=e.transform,n=e.containerWidth,r=e.iconWidth;return{outer:{transform:`translate(${n/2} 256)`},inner:{transform:`${`translate(${t.x*32}, ${t.y*32}) `} ${`scale(${t.size/16*(t.flipX?-1:1)}, ${t.size/16*(t.flipY?-1:1)}) `} ${`rotate(${t.rotate} 0 0)`}`},path:{transform:`translate(${r/2*-1} -256)`}}}function ln(e){var t=e.transform,n=e.width,r=n===void 0?Ct:n,i=e.height,a=i===void 0?Ct:i,o=e.startCentered,s=o===void 0?!1:o,c=``;return s&&fe?c+=`translate(${t.x/N-r/2}em, ${t.y/N-a/2}em) `:s?c+=`translate(calc(-50% + ${t.x/N}em), calc(-50% + ${t.y/N}em)) `:c+=`translate(${t.x/N}em, ${t.y/N}em) `,c+=`scale(${t.size/N*(t.flipX?-1:1)}, ${t.size/N*(t.flipY?-1:1)}) `,c+=`rotate(${t.rotate}deg) `,c}var un=`:root, :host {
  --fa-font-solid: normal 900 1em/1 "Font Awesome 7 Free";
  --fa-font-regular: normal 400 1em/1 "Font Awesome 7 Free";
  --fa-font-light: normal 300 1em/1 "Font Awesome 7 Pro";
  --fa-font-thin: normal 100 1em/1 "Font Awesome 7 Pro";
  --fa-font-duotone: normal 900 1em/1 "Font Awesome 7 Duotone";
  --fa-font-duotone-regular: normal 400 1em/1 "Font Awesome 7 Duotone";
  --fa-font-duotone-light: normal 300 1em/1 "Font Awesome 7 Duotone";
  --fa-font-duotone-thin: normal 100 1em/1 "Font Awesome 7 Duotone";
  --fa-font-brands: normal 400 1em/1 "Font Awesome 7 Brands";
  --fa-font-sharp-solid: normal 900 1em/1 "Font Awesome 7 Sharp";
  --fa-font-sharp-regular: normal 400 1em/1 "Font Awesome 7 Sharp";
  --fa-font-sharp-light: normal 300 1em/1 "Font Awesome 7 Sharp";
  --fa-font-sharp-thin: normal 100 1em/1 "Font Awesome 7 Sharp";
  --fa-font-sharp-duotone-solid: normal 900 1em/1 "Font Awesome 7 Sharp Duotone";
  --fa-font-sharp-duotone-regular: normal 400 1em/1 "Font Awesome 7 Sharp Duotone";
  --fa-font-sharp-duotone-light: normal 300 1em/1 "Font Awesome 7 Sharp Duotone";
  --fa-font-sharp-duotone-thin: normal 100 1em/1 "Font Awesome 7 Sharp Duotone";
  --fa-font-slab-regular: normal 400 1em/1 "Font Awesome 7 Slab";
  --fa-font-slab-press-regular: normal 400 1em/1 "Font Awesome 7 Slab Press";
  --fa-font-whiteboard-semibold: normal 600 1em/1 "Font Awesome 7 Whiteboard";
  --fa-font-thumbprint-light: normal 300 1em/1 "Font Awesome 7 Thumbprint";
  --fa-font-notdog-solid: normal 900 1em/1 "Font Awesome 7 Notdog";
  --fa-font-notdog-duo-solid: normal 900 1em/1 "Font Awesome 7 Notdog Duo";
  --fa-font-etch-solid: normal 900 1em/1 "Font Awesome 7 Etch";
  --fa-font-jelly-regular: normal 400 1em/1 "Font Awesome 7 Jelly";
  --fa-font-jelly-fill-regular: normal 400 1em/1 "Font Awesome 7 Jelly Fill";
  --fa-font-jelly-duo-regular: normal 400 1em/1 "Font Awesome 7 Jelly Duo";
  --fa-font-chisel-regular: normal 400 1em/1 "Font Awesome 7 Chisel";
  --fa-font-utility-semibold: normal 600 1em/1 "Font Awesome 7 Utility";
  --fa-font-utility-duo-semibold: normal 600 1em/1 "Font Awesome 7 Utility Duo";
  --fa-font-utility-fill-semibold: normal 600 1em/1 "Font Awesome 7 Utility Fill";
}

.svg-inline--fa {
  box-sizing: content-box;
  display: var(--fa-display, inline-block);
  height: 1em;
  overflow: visible;
  vertical-align: -0.125em;
  width: var(--fa-width, 1.25em);
}
.svg-inline--fa.fa-2xs {
  vertical-align: 0.1em;
}
.svg-inline--fa.fa-xs {
  vertical-align: 0em;
}
.svg-inline--fa.fa-sm {
  vertical-align: -0.0714285714em;
}
.svg-inline--fa.fa-lg {
  vertical-align: -0.2em;
}
.svg-inline--fa.fa-xl {
  vertical-align: -0.25em;
}
.svg-inline--fa.fa-2xl {
  vertical-align: -0.3125em;
}
.svg-inline--fa.fa-pull-left,
.svg-inline--fa .fa-pull-start {
  float: inline-start;
  margin-inline-end: var(--fa-pull-margin, 0.3em);
}
.svg-inline--fa.fa-pull-right,
.svg-inline--fa .fa-pull-end {
  float: inline-end;
  margin-inline-start: var(--fa-pull-margin, 0.3em);
}
.svg-inline--fa.fa-li {
  width: var(--fa-li-width, 2em);
  inset-inline-start: calc(-1 * var(--fa-li-width, 2em));
  inset-block-start: 0.25em; /* syncing vertical alignment with Web Font rendering */
}

.fa-layers-counter, .fa-layers-text {
  display: inline-block;
  position: absolute;
  text-align: center;
}

.fa-layers {
  display: inline-block;
  height: 1em;
  position: relative;
  text-align: center;
  vertical-align: -0.125em;
  width: var(--fa-width, 1.25em);
}
.fa-layers .svg-inline--fa {
  inset: 0;
  margin: auto;
  position: absolute;
  transform-origin: center center;
}

.fa-layers-text {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  transform-origin: center center;
}

.fa-layers-counter {
  background-color: var(--fa-counter-background-color, #ff253a);
  border-radius: var(--fa-counter-border-radius, 1em);
  box-sizing: border-box;
  color: var(--fa-inverse, #fff);
  line-height: var(--fa-counter-line-height, 1);
  max-width: var(--fa-counter-max-width, 5em);
  min-width: var(--fa-counter-min-width, 1.5em);
  overflow: hidden;
  padding: var(--fa-counter-padding, 0.25em 0.5em);
  right: var(--fa-right, 0);
  text-overflow: ellipsis;
  top: var(--fa-top, 0);
  transform: scale(var(--fa-counter-scale, 0.25));
  transform-origin: top right;
}

.fa-layers-bottom-right {
  bottom: var(--fa-bottom, 0);
  right: var(--fa-right, 0);
  top: auto;
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: bottom right;
}

.fa-layers-bottom-left {
  bottom: var(--fa-bottom, 0);
  left: var(--fa-left, 0);
  right: auto;
  top: auto;
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: bottom left;
}

.fa-layers-top-right {
  top: var(--fa-top, 0);
  right: var(--fa-right, 0);
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: top right;
}

.fa-layers-top-left {
  left: var(--fa-left, 0);
  right: auto;
  top: var(--fa-top, 0);
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: top left;
}

.fa-1x {
  font-size: 1em;
}

.fa-2x {
  font-size: 2em;
}

.fa-3x {
  font-size: 3em;
}

.fa-4x {
  font-size: 4em;
}

.fa-5x {
  font-size: 5em;
}

.fa-6x {
  font-size: 6em;
}

.fa-7x {
  font-size: 7em;
}

.fa-8x {
  font-size: 8em;
}

.fa-9x {
  font-size: 9em;
}

.fa-10x {
  font-size: 10em;
}

.fa-2xs {
  font-size: calc(10 / 16 * 1em); /* converts a 10px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 10 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 10 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-xs {
  font-size: calc(12 / 16 * 1em); /* converts a 12px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 12 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 12 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-sm {
  font-size: calc(14 / 16 * 1em); /* converts a 14px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 14 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 14 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-lg {
  font-size: calc(20 / 16 * 1em); /* converts a 20px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 20 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 20 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-xl {
  font-size: calc(24 / 16 * 1em); /* converts a 24px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 24 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 24 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-2xl {
  font-size: calc(32 / 16 * 1em); /* converts a 32px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 32 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 32 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-width-auto {
  --fa-width: auto;
}

.fa-fw,
.fa-width-fixed {
  --fa-width: 1.25em;
}

.fa-ul {
  list-style-type: none;
  margin-inline-start: var(--fa-li-margin, 2.5em);
  padding-inline-start: 0;
}
.fa-ul > li {
  position: relative;
}

.fa-li {
  inset-inline-start: calc(-1 * var(--fa-li-width, 2em));
  position: absolute;
  text-align: center;
  width: var(--fa-li-width, 2em);
  line-height: inherit;
}

/* Heads Up: Bordered Icons will not be supported in the future!
  - This feature will be deprecated in the next major release of Font Awesome (v8)!
  - You may continue to use it in this version *v7), but it will not be supported in Font Awesome v8.
*/
/* Notes:
* --@{v.$css-prefix}-border-width = 1/16 by default (to render as ~1px based on a 16px default font-size)
* --@{v.$css-prefix}-border-padding =
  ** 3/16 for vertical padding (to give ~2px of vertical whitespace around an icon considering it's vertical alignment)
  ** 4/16 for horizontal padding (to give ~4px of horizontal whitespace around an icon)
*/
.fa-border {
  border-color: var(--fa-border-color, #eee);
  border-radius: var(--fa-border-radius, 0.1em);
  border-style: var(--fa-border-style, solid);
  border-width: var(--fa-border-width, 0.0625em);
  box-sizing: var(--fa-border-box-sizing, content-box);
  padding: var(--fa-border-padding, 0.1875em 0.25em);
}

.fa-pull-left,
.fa-pull-start {
  float: inline-start;
  margin-inline-end: var(--fa-pull-margin, 0.3em);
}

.fa-pull-right,
.fa-pull-end {
  float: inline-end;
  margin-inline-start: var(--fa-pull-margin, 0.3em);
}

.fa-beat {
  animation-name: fa-beat;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-bounce {
  animation-name: fa-bounce;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.28, 0.84, 0.42, 1));
}

.fa-fade {
  animation-name: fa-fade;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-beat-fade {
  animation-name: fa-beat-fade;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-flip {
  animation-name: fa-flip;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-shake {
  animation-name: fa-shake;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin {
  animation-name: fa-spin;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 2s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin-reverse {
  --fa-animation-direction: reverse;
}

.fa-pulse,
.fa-spin-pulse {
  animation-name: fa-spin;
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, steps(8));
}

@media (prefers-reduced-motion: reduce) {
  .fa-beat,
  .fa-bounce,
  .fa-fade,
  .fa-beat-fade,
  .fa-flip,
  .fa-pulse,
  .fa-shake,
  .fa-spin,
  .fa-spin-pulse {
    animation: none !important;
    transition: none !important;
  }
}
@keyframes fa-beat {
  0%, 90% {
    transform: scale(1);
  }
  45% {
    transform: scale(var(--fa-beat-scale, 1.25));
  }
}
@keyframes fa-bounce {
  0% {
    transform: scale(1, 1) translateY(0);
  }
  10% {
    transform: scale(var(--fa-bounce-start-scale-x, 1.1), var(--fa-bounce-start-scale-y, 0.9)) translateY(0);
  }
  30% {
    transform: scale(var(--fa-bounce-jump-scale-x, 0.9), var(--fa-bounce-jump-scale-y, 1.1)) translateY(var(--fa-bounce-height, -0.5em));
  }
  50% {
    transform: scale(var(--fa-bounce-land-scale-x, 1.05), var(--fa-bounce-land-scale-y, 0.95)) translateY(0);
  }
  57% {
    transform: scale(1, 1) translateY(var(--fa-bounce-rebound, -0.125em));
  }
  64% {
    transform: scale(1, 1) translateY(0);
  }
  100% {
    transform: scale(1, 1) translateY(0);
  }
}
@keyframes fa-fade {
  50% {
    opacity: var(--fa-fade-opacity, 0.4);
  }
}
@keyframes fa-beat-fade {
  0%, 100% {
    opacity: var(--fa-beat-fade-opacity, 0.4);
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(var(--fa-beat-fade-scale, 1.125));
  }
}
@keyframes fa-flip {
  50% {
    transform: rotate3d(var(--fa-flip-x, 0), var(--fa-flip-y, 1), var(--fa-flip-z, 0), var(--fa-flip-angle, -180deg));
  }
}
@keyframes fa-shake {
  0% {
    transform: rotate(-15deg);
  }
  4% {
    transform: rotate(15deg);
  }
  8%, 24% {
    transform: rotate(-18deg);
  }
  12%, 28% {
    transform: rotate(18deg);
  }
  16% {
    transform: rotate(-22deg);
  }
  20% {
    transform: rotate(22deg);
  }
  32% {
    transform: rotate(-12deg);
  }
  36% {
    transform: rotate(12deg);
  }
  40%, 100% {
    transform: rotate(0deg);
  }
}
@keyframes fa-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.fa-rotate-90 {
  transform: rotate(90deg);
}

.fa-rotate-180 {
  transform: rotate(180deg);
}

.fa-rotate-270 {
  transform: rotate(270deg);
}

.fa-flip-horizontal {
  transform: scale(-1, 1);
}

.fa-flip-vertical {
  transform: scale(1, -1);
}

.fa-flip-both,
.fa-flip-horizontal.fa-flip-vertical {
  transform: scale(-1, -1);
}

.fa-rotate-by {
  transform: rotate(var(--fa-rotate-angle, 0));
}

.svg-inline--fa .fa-primary {
  fill: var(--fa-primary-color, currentColor);
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa .fa-secondary {
  fill: var(--fa-secondary-color, currentColor);
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-primary {
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-secondary {
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa mask .fa-primary,
.svg-inline--fa mask .fa-secondary {
  fill: black;
}

.svg-inline--fa.fa-inverse {
  fill: var(--fa-inverse, #fff);
}

.fa-stack {
  display: inline-block;
  height: 2em;
  line-height: 2em;
  position: relative;
  vertical-align: middle;
  width: 2.5em;
}

.fa-inverse {
  color: var(--fa-inverse, #fff);
}

.svg-inline--fa.fa-stack-1x {
  --fa-width: 1.25em;
  height: 1em;
  width: var(--fa-width);
}
.svg-inline--fa.fa-stack-2x {
  --fa-width: 2.5em;
  height: 2em;
  width: var(--fa-width);
}

.fa-stack-1x,
.fa-stack-2x {
  inset: 0;
  margin: auto;
  position: absolute;
  z-index: var(--fa-stack-z-index, auto);
}`;function dn(){var e=wt,t=Tt,n=j.cssPrefix,r=j.replacementClass,i=un;if(n!==e||r!==t){var a=RegExp(`\\.${e}\\-`,`g`),o=RegExp(`\\--${e}\\-`,`g`),s=RegExp(`\\.${t}`,`g`);i=i.replace(a,`.${n}-`).replace(o,`--${n}-`).replace(s,`.${r}`)}return i}var fn=!1;function pn(){j.autoAddCss&&!fn&&($t(dn()),fn=!0)}var mn={mixout:function(){return{dom:{css:dn,insertCss:pn}}},hooks:function(){return{beforeDOMElementCreation:function(){pn()},beforeI2svg:function(){pn()}}}},I=S||{};I[D]||(I[D]={}),I[D].styles||(I[D].styles={}),I[D].hooks||(I[D].hooks={}),I[D].shims||(I[D].shims=[]);var L=I[D],hn=[],gn=function(){C.removeEventListener(`DOMContentLoaded`,gn),_n=1,hn.map(function(e){return e()})},_n=!1;w&&(_n=(C.documentElement.doScroll?/^loaded|^c/:/^loaded|^i|^c/).test(C.readyState),_n||C.addEventListener(`DOMContentLoaded`,gn));function vn(e){w&&(_n?setTimeout(e,0):hn.push(e))}function R(e){var t=e.tag,n=e.attributes,r=n===void 0?{}:n,i=e.children,a=i===void 0?[]:i;return typeof e==`string`?rn(e):`<${t} ${an(r)}>${a.map(R).join(``)}</${t}>`}function yn(e,t,n){if(e&&e[t]&&e[t][n])return{prefix:t,iconName:n,icon:e[t][n]}}var bn=function(e,t){return function(n,r,i,a){return e.call(t,n,r,i,a)}},xn=function(e,t,n,r){var i=Object.keys(e),a=i.length,o=r===void 0?t:bn(t,r),s,c,l;for(n===void 0?(s=1,l=e[i[0]]):(s=0,l=n);s<a;s++)c=i[s],l=o(l,e[c],c,e);return l};function Sn(e){return b(e).length===1?e.codePointAt(0).toString(16):null}function Cn(e){return Object.keys(e).reduce(function(t,n){var r=e[n];return r.icon?t[r.iconName]=r.icon:t[n]=r,t},{})}function wn(e,t){var n=(arguments.length>2&&arguments[2]!==void 0?arguments[2]:{}).skipHooks,r=n===void 0?!1:n,i=Cn(t);typeof L.hooks.addPack==`function`&&!r?L.hooks.addPack(e,Cn(t)):L.styles[e]=v(v({},L.styles[e]||{}),i),e===`fas`&&wn(`fa`,t)}var z=L.styles,Tn=L.shims,En=Object.keys(Vt),Dn=En.reduce(function(e,t){return e[t]=Object.keys(Vt[t]),e},{}),On=null,kn={},An={},jn={},Mn={},Nn={};function Pn(e){return~Jt.indexOf(e)}function Fn(e,t){var n=t.split(`-`),r=n[0],i=n.slice(1).join(`-`);return r===e&&i!==``&&!Pn(i)?i:null}var In=function(){var e=function(e){return xn(z,function(t,n,r){return t[r]=xn(n,e,{}),t},{})};kn=e(function(e,t,n){return t[3]&&(e[t[3]]=n),t[2]&&t[2].filter(function(e){return typeof e==`number`}).forEach(function(t){e[t.toString(16)]=n}),e}),An=e(function(e,t,n){return e[n]=n,t[2]&&t[2].filter(function(e){return typeof e==`string`}).forEach(function(t){e[t]=n}),e}),Nn=e(function(e,t,n){var r=t[2];return e[n]=n,r.forEach(function(t){e[t]=n}),e});var t=`far`in z||j.autoFetchSvg,n=xn(Tn,function(e,n){var r=n[0],i=n[1],a=n[2];return i===`far`&&!t&&(i=`fas`),typeof r==`string`&&(e.names[r]={prefix:i,iconName:a}),typeof r==`number`&&(e.unicodes[r.toString(16)]={prefix:i,iconName:a}),e},{names:{},unicodes:{}});jn=n.names,Mn=n.unicodes,On=Un(j.styleDefault,{family:j.familyDefault})};Qt(function(e){On=Un(e.styleDefault,{family:j.familyDefault})}),In();function Ln(e,t){return(kn[e]||{})[t]}function Rn(e,t){return(An[e]||{})[t]}function B(e,t){return(Nn[e]||{})[t]}function zn(e){return jn[e]||{prefix:null,iconName:null}}function Bn(e){var t=Mn[e],n=Ln(`fas`,e);return t||(n?{prefix:`fas`,iconName:n}:null)||{prefix:null,iconName:null}}function V(){return On}var Vn=function(){return{prefix:null,iconName:null,rest:[]}};function Hn(e){var t=T,n=En.reduce(function(e,t){return e[t]=`${j.cssPrefix}-${t}`,e},{});return $e.forEach(function(r){(e.includes(n[r])||e.some(function(e){return Dn[r].includes(e)}))&&(t=r)}),t}function Un(e){var t=(arguments.length>1&&arguments[1]!==void 0?arguments[1]:{}).family,n=t===void 0?T:t,r=Lt[n][e];if(n===E&&!e)return`fad`;var i=zt[n][e]||zt[n][r],a=e in L.styles?e:null;return i||a||null}function Wn(e){var t=[],n=null;return e.forEach(function(e){var r=Fn(j.cssPrefix,e);r?n=r:e&&t.push(e)}),{iconName:n,rest:t}}function Gn(e){return e.sort().filter(function(e,t,n){return n.indexOf(e)===t})}var Kn=_t.concat(it);function qn(e){var t=(arguments.length>1&&arguments[1]!==void 0?arguments[1]:{}).skipLookups,n=t===void 0?!1:t,r=null,i=Gn(e.filter(function(e){return Kn.includes(e)})),a=Gn(e.filter(function(e){return!Kn.includes(e)})),o=y(i.filter(function(e){return r=e,!ve.includes(e)}),1)[0],s=o===void 0?null:o,c=Hn(i),l=v(v({},Wn(a)),{},{prefix:Un(s,{family:c})});return v(v(v({},l),Zn({values:e,family:c,styles:z,config:j,canonical:l,givenPrefix:r})),Jn(n,r,l))}function Jn(e,t,n){var r=n.prefix,i=n.iconName;if(e||!r||!i)return{prefix:r,iconName:i};var a=t===`fa`?zn(i):{},o=B(r,i);return i=a.iconName||o||i,r=a.prefix||r,r===`far`&&!z.far&&z.fas&&!j.autoFetchSvg&&(r=`fas`),{prefix:r,iconName:i}}var Yn=$e.filter(function(e){return e!==T||e!==E}),Xn=Object.keys(gt).filter(function(e){return e!==T}).map(function(e){return Object.keys(gt[e])}).flat();function Zn(e){var t=e.values,n=e.family,r=e.canonical,i=e.givenPrefix,a=i===void 0?``:i,o=e.styles,s=o===void 0?{}:o,c=e.config,l=c===void 0?{}:c,u=n===E,d=t.includes(`fa-duotone`)||t.includes(`fad`),f=l.familyDefault===`duotone`,p=r.prefix===`fad`||r.prefix===`fa-duotone`;return!u&&(d||f||p)&&(r.prefix=`fad`),(t.includes(`fa-brands`)||t.includes(`fab`))&&(r.prefix=`fab`),!r.prefix&&Yn.includes(n)&&(Object.keys(s).find(function(e){return Xn.includes(e)})||l.autoFetchSvg)&&(r.prefix=nt.get(n).defaultShortPrefixId,r.iconName=B(r.prefix,r.iconName)||r.iconName),(r.prefix===`fa`||a===`fa`)&&(r.prefix=V()||`fas`),r}var Qn=function(){function e(){c(this,e),this.definitions={}}return u(e,[{key:`add`,value:function(){var e=this,t=[...arguments].reduce(this._pullDefinitions,{});Object.keys(t).forEach(function(n){e.definitions[n]=v(v({},e.definitions[n]||{}),t[n]),wn(n,t[n]);var r=Vt[T][n];r&&wn(r,t[n]),In()})}},{key:`reset`,value:function(){this.definitions={}}},{key:`_pullDefinitions`,value:function(e,t){var n=t.prefix&&t.iconName&&t.icon?{0:t}:t;return Object.keys(n).map(function(t){var r=n[t],i=r.prefix,a=r.iconName,o=r.icon,s=o[2];e[i]||(e[i]={}),s.length>0&&s.forEach(function(t){typeof t==`string`&&(e[i][t]=o)}),e[i][a]=o}),e}}])}(),$n=[],H={},U={},er=Object.keys(U);function tr(e,t){var n=t.mixoutsTo;return $n=e,H={},Object.keys(U).forEach(function(e){er.indexOf(e)===-1&&delete U[e]}),$n.forEach(function(e){var t=e.mixout?e.mixout():{};if(Object.keys(t).forEach(function(e){typeof t[e]==`function`&&(n[e]=t[e]),te(t[e])===`object`&&Object.keys(t[e]).forEach(function(r){n[e]||(n[e]={}),n[e][r]=t[e][r]})}),e.hooks){var r=e.hooks();Object.keys(r).forEach(function(e){H[e]||(H[e]=[]),H[e].push(r[e])})}e.provides&&e.provides(U)}),n}function nr(e,t){var n=[...arguments].slice(2);return(H[e]||[]).forEach(function(e){t=e.apply(null,[t].concat(n))}),t}function W(e){var t=[...arguments].slice(1);(H[e]||[]).forEach(function(e){e.apply(null,t)})}function G(){var e=arguments[0],t=Array.prototype.slice.call(arguments,1);return U[e]?U[e].apply(null,t):void 0}function rr(e){e.prefix===`fa`&&(e.prefix=`fas`);var t=e.iconName,n=e.prefix||V();if(t)return t=B(n,t)||t,yn(ir.definitions,n,t)||yn(L.styles,n,t)}var ir=new Qn,K={noAuto:function(){j.autoReplaceSvg=!1,j.observeMutations=!1,W(`noAuto`)},config:j,dom:{i2svg:function(){var e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};return w?(W(`beforeI2svg`,e),G(`pseudoElements2svg`,e),G(`i2svg`,e)):Promise.reject(Error(`Operation requires a DOM of some kind.`))},watch:function(){var e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},t=e.autoReplaceSvgRoot;j.autoReplaceSvg===!1&&(j.autoReplaceSvg=!0),j.observeMutations=!0,vn(function(){ar({autoReplaceSvgRoot:t}),W(`watch`,e)})}},parse:{icon:function(e){if(e===null)return null;if(te(e)===`object`&&e.prefix&&e.iconName)return{prefix:e.prefix,iconName:B(e.prefix,e.iconName)||e.iconName};if(Array.isArray(e)&&e.length===2){var t=e[1].indexOf(`fa-`)===0?e[1].slice(3):e[1],n=Un(e[0]);return{prefix:n,iconName:B(n,t)||t}}if(typeof e==`string`&&(e.indexOf(`${j.cssPrefix}-`)>-1||e.match(Ut))){var r=qn(e.split(` `),{skipLookups:!0});return{prefix:r.prefix||V(),iconName:B(r.prefix,r.iconName)||r.iconName}}if(typeof e==`string`){var i=V();return{prefix:i,iconName:B(i,e)||e}}}},library:ir,findIconDefinition:rr,toHtml:R},ar=function(){var e=(arguments.length>0&&arguments[0]!==void 0?arguments[0]:{}).autoReplaceSvgRoot,t=e===void 0?C:e;(Object.keys(L.styles).length>0||j.autoFetchSvg)&&w&&j.autoReplaceSvg&&K.dom.i2svg({node:t})};function or(e,t){return Object.defineProperty(e,`abstract`,{get:t}),Object.defineProperty(e,`html`,{get:function(){return e.abstract.map(function(e){return R(e)})}}),Object.defineProperty(e,`node`,{get:function(){if(w){var t=C.createElement(`div`);return t.innerHTML=e.html,t.children}}}),e}function sr(e){var t=e.children,n=e.main,r=e.mask,i=e.attributes,a=e.styles,o=e.transform;if(sn(o)&&n.found&&!r.found){var s={x:n.width/n.height/2,y:.5};i.style=on(v(v({},a),{},{"transform-origin":`${s.x+o.x/16}em ${s.y+o.y/16}em`}))}return[{tag:`svg`,attributes:i,children:t}]}function cr(e){var t=e.prefix,n=e.iconName,r=e.children,i=e.attributes,a=e.symbol,o=a===!0?`${t}-${j.cssPrefix}-${n}`:a;return[{tag:`svg`,attributes:{style:`display: none;`},children:[{tag:`symbol`,attributes:v(v({},i),{},{id:o}),children:r}]}]}function lr(e){return[`aria-label`,`aria-labelledby`,`title`,`role`].some(function(t){return t in e})}function ur(e){var t=e.icons,n=t.main,r=t.mask,i=e.prefix,a=e.iconName,o=e.transform,s=e.symbol,c=e.maskId,l=e.extra,u=e.watchable,d=u===void 0?!1:u,f=r.found?r:n,p=f.width,m=f.height,h=[j.replacementClass,a?`${j.cssPrefix}-${a}`:``].filter(function(e){return l.classes.indexOf(e)===-1}).filter(function(e){return e!==``||!!e}).concat(l.classes).join(` `),g={children:[],attributes:v(v({},l.attributes),{},{"data-prefix":i,"data-icon":a,class:h,role:l.attributes.role||`img`,viewBox:`0 0 ${p} ${m}`})};!lr(l.attributes)&&!l.attributes[`aria-hidden`]&&(g.attributes[`aria-hidden`]=`true`),d&&(g.attributes[O]=``);var _=v(v({},g),{},{prefix:i,iconName:a,main:n,mask:r,maskId:c,transform:o,symbol:s,styles:v({},l.styles)}),y=r.found&&n.found?G(`generateAbstractMask`,_)||{children:[],attributes:{}}:G(`generateAbstractIcon`,_)||{children:[],attributes:{}},b=y.children,x=y.attributes;return _.children=b,_.attributes=x,s?cr(_):sr(_)}function dr(e){var t=e.content,n=e.width,r=e.height,i=e.transform,a=e.extra,o=e.watchable,s=o===void 0?!1:o,c=v(v({},a.attributes),{},{class:a.classes.join(` `)});s&&(c[O]=``);var l=v({},a.styles);sn(i)&&(l.transform=ln({transform:i,startCentered:!0,width:n,height:r}),l[`-webkit-transform`]=l.transform);var u=on(l);u.length>0&&(c.style=u);var d=[];return d.push({tag:`span`,attributes:c,children:[t]}),d}function fr(e){var t=e.content,n=e.extra,r=v(v({},n.attributes),{},{class:n.classes.join(` `)}),i=on(n.styles);i.length>0&&(r.style=i);var a=[];return a.push({tag:`span`,attributes:r,children:[t]}),a}var pr=L.styles;function mr(e){var t=e[0],n=e[1],r=y(e.slice(4),1)[0],i=null;return i=Array.isArray(r)?{tag:`g`,attributes:{class:`${j.cssPrefix}-${qt.GROUP}`},children:[{tag:`path`,attributes:{class:`${j.cssPrefix}-${qt.SECONDARY}`,fill:`currentColor`,d:r[0]}},{tag:`path`,attributes:{class:`${j.cssPrefix}-${qt.PRIMARY}`,fill:`currentColor`,d:r[1]}}]}:{tag:`path`,attributes:{fill:`currentColor`,d:r}},{found:!0,width:t,height:n,icon:i}}var hr={found:!1,width:512,height:512};function gr(e,t){!Pt&&!j.showMissingIcons&&e&&console.error(`Icon with name "${e}" and prefix "${t}" is missing.`)}function _r(e,t){var n=t;return t===`fa`&&j.styleDefault!==null&&(t=V()),new Promise(function(r,i){if(n===`fa`){var a=zn(e)||{};e=a.iconName||e,t=a.prefix||t}if(e&&t&&pr[t]&&pr[t][e]){var o=pr[t][e];return r(mr(o))}gr(e,t),r(v(v({},hr),{},{icon:j.showMissingIcons&&e&&G(`missingIconAbstract`)||{}}))})}var vr=function(){},yr=j.measurePerformance&&de&&de.mark&&de.measure?de:{mark:vr,measure:vr},q=`FA "7.1.0"`,br=function(e){return yr.mark(`${q} ${e} begins`),function(){return xr(e)}},xr=function(e){yr.mark(`${q} ${e} ends`),yr.measure(`${q} ${e}`,`${q} ${e} begins`,`${q} ${e} ends`)},Sr={begin:br,end:xr},Cr=function(){};function wr(e){return typeof(e.getAttribute?e.getAttribute(O):null)==`string`}function Tr(e){var t=e.getAttribute?e.getAttribute(Ot):null,n=e.getAttribute?e.getAttribute(kt):null;return t&&n}function Er(e){return e&&e.classList&&e.classList.contains&&e.classList.contains(j.replacementClass)}function Dr(){return j.autoReplaceSvg===!0?Mr.replace:Mr[j.autoReplaceSvg]||Mr.replace}function Or(e){return C.createElementNS(`http://www.w3.org/2000/svg`,e)}function kr(e){return C.createElement(e)}function Ar(e){var t=(arguments.length>1&&arguments[1]!==void 0?arguments[1]:{}).ceFn,n=t===void 0?e.tag===`svg`?Or:kr:t;if(typeof e==`string`)return C.createTextNode(e);var r=n(e.tag);return Object.keys(e.attributes||[]).forEach(function(t){r.setAttribute(t,e.attributes[t])}),(e.children||[]).forEach(function(e){r.appendChild(Ar(e,{ceFn:n}))}),r}function jr(e){var t=` ${e.outerHTML} `;return t=`${t}Font Awesome fontawesome.com `,t}var Mr={replace:function(e){var t=e[0];if(t.parentNode)if(e[1].forEach(function(e){t.parentNode.insertBefore(Ar(e),t)}),t.getAttribute(O)===null&&j.keepOriginalSource){var n=C.createComment(jr(t));t.parentNode.replaceChild(n,t)}else t.remove()},nest:function(e){var t=e[0],n=e[1];if(~nn(t).indexOf(j.replacementClass))return Mr.replace(e);var r=RegExp(`${j.cssPrefix}-.*`);if(delete n[0].attributes.id,n[0].attributes.class){var i=n[0].attributes.class.split(` `).reduce(function(e,t){return t===j.replacementClass||t.match(r)?e.toSvg.push(t):e.toNode.push(t),e},{toNode:[],toSvg:[]});n[0].attributes.class=i.toSvg.join(` `),i.toNode.length===0?t.removeAttribute(`class`):t.setAttribute(`class`,i.toNode.join(` `))}var a=n.map(function(e){return R(e)}).join(`
`);t.setAttribute(O,``),t.innerHTML=a}};function Nr(e){e()}function Pr(e,t){var n=typeof t==`function`?t:Cr;if(e.length===0)n();else{var r=Nr;j.mutateApproach===jt&&(r=S.requestAnimationFrame||Nr),r(function(){var t=Dr(),r=Sr.begin(`mutate`);e.map(t),r(),n()})}}var Fr=!1;function Ir(){Fr=!0}function Lr(){Fr=!1}var Rr=null;function zr(e){if(ue&&j.observeMutations){var t=e.treeCallback,n=t===void 0?Cr:t,r=e.nodeCallback,i=r===void 0?Cr:r,a=e.pseudoElementsCallback,o=a===void 0?Cr:a,s=e.observeMutationsRoot,c=s===void 0?C:s;Rr=new ue(function(e){if(!Fr){var t=V();F(e).forEach(function(e){if(e.type===`childList`&&e.addedNodes.length>0&&!wr(e.addedNodes[0])&&(j.searchPseudoElements&&o(e.target),n(e.target)),e.type===`attributes`&&e.target.parentNode&&j.searchPseudoElements&&o([e.target],!0),e.type===`attributes`&&wr(e.target)&&~Kt.indexOf(e.attributeName))if(e.attributeName===`class`&&Tr(e.target)){var r=qn(nn(e.target)),a=r.prefix,s=r.iconName;e.target.setAttribute(Ot,a||t),s&&e.target.setAttribute(kt,s)}else Er(e.target)&&i(e.target)})}}),w&&Rr.observe(c,{childList:!0,attributes:!0,characterData:!0,subtree:!0})}}function Br(){Rr&&Rr.disconnect()}function Vr(e){var t=e.getAttribute(`style`),n=[];return t&&(n=t.split(`;`).reduce(function(e,t){var n=t.split(`:`),r=n[0],i=n.slice(1);return r&&i.length>0&&(e[r]=i.join(`:`).trim()),e},{})),n}function Hr(e){var t=e.getAttribute(`data-prefix`),n=e.getAttribute(`data-icon`),r=e.innerText===void 0?``:e.innerText.trim(),i=qn(nn(e));return i.prefix||=V(),t&&n&&(i.prefix=t,i.iconName=n),i.iconName&&i.prefix?i:(i.prefix&&r.length>0&&(i.iconName=Rn(i.prefix,e.innerText)||Ln(i.prefix,Sn(e.innerText))),!i.iconName&&j.autoFetchSvg&&e.firstChild&&e.firstChild.nodeType===Node.TEXT_NODE&&(i.iconName=e.firstChild.data),i)}function Ur(e){return F(e.attributes).reduce(function(e,t){return e.name!==`class`&&e.name!==`style`&&(e[t.name]=t.value),e},{})}function Wr(){return{iconName:null,prefix:null,transform:P,symbol:!1,mask:{iconName:null,prefix:null,rest:[]},maskId:null,extra:{classes:[],styles:{},attributes:{}}}}function Gr(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{styleParser:!0},n=Hr(e),r=n.iconName,i=n.prefix,a=n.rest,o=Ur(e),s=nr(`parseNodeAttributes`,{},e);return v({iconName:r,prefix:i,transform:P,mask:{iconName:null,prefix:null,rest:[]},maskId:null,symbol:!1,extra:{classes:a,styles:t.styleParser?Vr(e):[],attributes:o}},s)}var Kr=L.styles;function qr(e){var t=j.autoReplaceSvg===`nest`?Gr(e,{styleParser:!1}):Gr(e);return~t.extra.classes.indexOf(Wt)?G(`generateLayersText`,e,t):G(`generateSvgReplacementMutation`,e,t)}function Jr(){return[].concat(b(it),b(_t))}function Yr(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;if(!w)return Promise.resolve();var n=C.documentElement.classList,r=function(e){return n.add(`${At}-${e}`)},i=function(e){return n.remove(`${At}-${e}`)},a=j.autoFetchSvg?Jr():ve.concat(Object.keys(Kr));a.includes(`fa`)||a.push(`fa`);var o=[`.${Wt}:not([${O}])`].concat(a.map(function(e){return`.${e}:not([${O}])`})).join(`, `);if(o.length===0)return Promise.resolve();var s=[];try{s=F(e.querySelectorAll(o))}catch{}if(s.length>0)r(`pending`),i(`complete`);else return Promise.resolve();var c=Sr.begin(`onTree`),l=s.reduce(function(e,t){try{var n=qr(t);n&&e.push(n)}catch(e){Pt||e.name===`MissingIcon`&&console.error(e)}return e},[]);return new Promise(function(e,n){Promise.all(l).then(function(n){Pr(n,function(){r(`active`),r(`complete`),i(`pending`),typeof t==`function`&&t(),c(),e()})}).catch(function(e){c(),n(e)})})}function Xr(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;qr(e).then(function(e){e&&Pr([e],t)})}function Zr(e){return function(t){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},r=(t||{}).icon?t:rr(t||{}),i=n.mask;return i&&=(i||{}).icon?i:rr(i||{}),e(r,v(v({},n),{},{mask:i}))}}var Qr=function(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=t.transform,r=n===void 0?P:n,i=t.symbol,a=i===void 0?!1:i,o=t.mask,s=o===void 0?null:o,c=t.maskId,l=c===void 0?null:c,u=t.classes,d=u===void 0?[]:u,f=t.attributes,p=f===void 0?{}:f,m=t.styles,h=m===void 0?{}:m;if(e){var g=e.prefix,_=e.iconName,y=e.icon;return or(v({type:`icon`},e),function(){return W(`beforeDOMElementCreation`,{iconDefinition:e,params:t}),ur({icons:{main:mr(y),mask:s?mr(s.icon):{found:!1,width:null,height:null,icon:{}}},prefix:g,iconName:_,transform:v(v({},P),r),symbol:a,maskId:l,extra:{attributes:p,styles:h,classes:d}})})}},$r={mixout:function(){return{icon:Zr(Qr)}},hooks:function(){return{mutationObserverCallbacks:function(e){return e.treeCallback=Yr,e.nodeCallback=Xr,e}}},provides:function(e){e.i2svg=function(e){var t=e.node,n=t===void 0?C:t,r=e.callback;return Yr(n,r===void 0?function(){}:r)},e.generateSvgReplacementMutation=function(e,t){var n=t.iconName,r=t.prefix,i=t.transform,a=t.symbol,o=t.mask,s=t.maskId,c=t.extra;return new Promise(function(t,l){Promise.all([_r(n,r),o.iconName?_r(o.iconName,o.prefix):Promise.resolve({found:!1,width:512,height:512,icon:{}})]).then(function(o){var l=y(o,2),u=l[0],d=l[1];t([e,ur({icons:{main:u,mask:d},prefix:r,iconName:n,transform:i,symbol:a,maskId:s,extra:c,watchable:!0})])}).catch(l)})},e.generateAbstractIcon=function(e){var t=e.children,n=e.attributes,r=e.main,i=e.transform,a=e.styles,o=on(a);o.length>0&&(n.style=o);var s;return sn(i)&&(s=G(`generateAbstractTransformGrouping`,{main:r,transform:i,containerWidth:r.width,iconWidth:r.width})),t.push(s||r.icon),{children:t,attributes:n}}}},ei={mixout:function(){return{layer:function(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=t.classes,r=n===void 0?[]:n;return or({type:`layer`},function(){W(`beforeDOMElementCreation`,{assembler:e,params:t});var n=[];return e(function(e){Array.isArray(e)?e.map(function(e){n=n.concat(e.abstract)}):n=n.concat(e.abstract)}),[{tag:`span`,attributes:{class:[`${j.cssPrefix}-layers`].concat(b(r)).join(` `)},children:n}]})}}}},ti={mixout:function(){return{counter:function(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=t.title,r=n===void 0?null:n,i=t.classes,a=i===void 0?[]:i,o=t.attributes,s=o===void 0?{}:o,c=t.styles,l=c===void 0?{}:c;return or({type:`counter`,content:e},function(){return W(`beforeDOMElementCreation`,{content:e,params:t}),fr({content:e.toString(),title:r,extra:{attributes:s,styles:l,classes:[`${j.cssPrefix}-layers-counter`].concat(b(a))}})})}}}},ni={mixout:function(){return{text:function(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=t.transform,r=n===void 0?P:n,i=t.classes,a=i===void 0?[]:i,o=t.attributes,s=o===void 0?{}:o,c=t.styles,l=c===void 0?{}:c;return or({type:`text`,content:e},function(){return W(`beforeDOMElementCreation`,{content:e,params:t}),dr({content:e,transform:v(v({},P),r),extra:{attributes:s,styles:l,classes:[`${j.cssPrefix}-layers-text`].concat(b(a))}})})}}},provides:function(e){e.generateLayersText=function(e,t){var n=t.transform,r=t.extra,i=null,a=null;if(fe){var o=parseInt(getComputedStyle(e).fontSize,10),s=e.getBoundingClientRect();i=s.width/o,a=s.height/o}return Promise.resolve([e,dr({content:e.innerHTML,width:i,height:a,transform:n,extra:r,watchable:!0})])}}},ri=RegExp(`"`,`ug`),ii=[1105920,1112319],ai=v(v(v(v({},{FontAwesome:{normal:`fas`,400:`fas`}}),tt),St),ct),oi=Object.keys(ai).reduce(function(e,t){return e[t.toLowerCase()]=ai[t],e},{}),si=Object.keys(oi).reduce(function(e,t){var n=oi[t];return e[t]=n[900]||b(Object.entries(n))[0][1],e},{});function ci(e){return Sn(b(e.replace(ri,``))[0]||``)}function li(e){var t=e.getPropertyValue(`font-feature-settings`).includes(`ss01`),n=e.getPropertyValue(`content`).replace(ri,``),r=n.codePointAt(0),i=r>=ii[0]&&r<=ii[1],a=n.length===2?n[0]===n[1]:!1;return i||a||t}function ui(e,t){var n=e.replace(/^['"]|['"]$/g,``).toLowerCase(),r=parseInt(t),i=isNaN(r)?`normal`:r;return(oi[n]||{})[i]||si[n]}function di(e,t){var n=`${Dt}${t.replace(`:`,`-`)}`;return new Promise(function(r,i){if(e.getAttribute(n)!==null)return r();var a=F(e.children).filter(function(e){return e.getAttribute(Et)===t})[0],o=S.getComputedStyle(e,t),s=o.getPropertyValue(`font-family`),c=s.match(Gt),l=o.getPropertyValue(`font-weight`),u=o.getPropertyValue(`content`);if(a&&!c)return e.removeChild(a),r();if(c&&u!==`none`&&u!==``){var d=o.getPropertyValue(`content`),f=ui(s,l),p=ci(d),m=c[0].startsWith(`FontAwesome`),h=li(o),g=Ln(f,p),_=g;if(m){var y=Bn(p);y.iconName&&y.prefix&&(g=y.iconName,f=y.prefix)}if(g&&!h&&(!a||a.getAttribute(Ot)!==f||a.getAttribute(kt)!==_)){e.setAttribute(n,_),a&&e.removeChild(a);var b=Wr(),x=b.extra;x.attributes[Et]=t,_r(g,f).then(function(i){var a=ur(v(v({},b),{},{icons:{main:i,mask:Vn()},prefix:f,iconName:_,extra:x,watchable:!0})),o=C.createElementNS(`http://www.w3.org/2000/svg`,`svg`);t===`::before`?e.insertBefore(o,e.firstChild):e.appendChild(o),o.outerHTML=a.map(function(e){return R(e)}).join(`
`),e.removeAttribute(n),r()}).catch(i)}else r()}else r()})}function fi(e){return Promise.all([di(e,`::before`),di(e,`::after`)])}function pi(e){return e.parentNode!==document.head&&!~Mt.indexOf(e.tagName.toUpperCase())&&!e.getAttribute(Et)&&(!e.parentNode||e.parentNode.tagName!==`svg`)}var mi=function(e){return!!e&&Nt.some(function(t){return e.includes(t)})},hi=function(e){if(!e)return[];var t=new Set,n=e.split(/,(?![^()]*\))/).map(function(e){return e.trim()});n=n.flatMap(function(e){return e.includes(`(`)?e:e.split(`,`).map(function(e){return e.trim()})});var r=d(n),i;try{for(r.s();!(i=r.n()).done;){var a=i.value;if(mi(a)){var o=Nt.reduce(function(e,t){return e.replace(t,``)},a);o!==``&&o!==`*`&&t.add(o)}}}catch(e){r.e(e)}finally{r.f()}return t};function gi(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1;if(w){var n;if(t)n=e;else if(j.searchPseudoElementsFullScan)n=e.querySelectorAll(`*`);else{var r=new Set,i=d(document.styleSheets),a;try{for(i.s();!(a=i.n()).done;){var o=a.value;try{var s=d(o.cssRules),c;try{for(s.s();!(c=s.n()).done;){var l=c.value,u=d(hi(l.selectorText)),f;try{for(u.s();!(f=u.n()).done;){var p=f.value;r.add(p)}}catch(e){u.e(e)}finally{u.f()}}}catch(e){s.e(e)}finally{s.f()}}catch(e){j.searchPseudoElementsWarnings&&console.warn(`Font Awesome: cannot parse stylesheet: ${o.href} (${e.message})
If it declares any Font Awesome CSS pseudo-elements, they will not be rendered as SVG icons. Add crossorigin="anonymous" to the <link>, enable searchPseudoElementsFullScan for slower but more thorough DOM parsing, or suppress this warning by setting searchPseudoElementsWarnings to false.`)}}}catch(e){i.e(e)}finally{i.f()}if(!r.size)return;var m=Array.from(r).join(`, `);try{n=e.querySelectorAll(m)}catch{}}return new Promise(function(e,t){var r=F(n).filter(pi).map(fi),i=Sr.begin(`searchPseudoElements`);Ir(),Promise.all(r).then(function(){i(),Lr(),e()}).catch(function(){i(),Lr(),t()})})}}var _i={hooks:function(){return{mutationObserverCallbacks:function(e){return e.pseudoElementsCallback=gi,e}}},provides:function(e){e.pseudoElements2svg=function(e){var t=e.node,n=t===void 0?C:t;j.searchPseudoElements&&gi(n)}}},vi=!1,yi={mixout:function(){return{dom:{unwatch:function(){Ir(),vi=!0}}}},hooks:function(){return{bootstrap:function(){zr(nr(`mutationObserverCallbacks`,{}))},noAuto:function(){Br()},watch:function(e){var t=e.observeMutationsRoot;vi?Lr():zr(nr(`mutationObserverCallbacks`,{observeMutationsRoot:t}))}}}},bi=function(e){return e.toLowerCase().split(` `).reduce(function(e,t){var n=t.toLowerCase().split(`-`),r=n[0],i=n.slice(1).join(`-`);if(r&&i===`h`)return e.flipX=!0,e;if(r&&i===`v`)return e.flipY=!0,e;if(i=parseFloat(i),isNaN(i))return e;switch(r){case`grow`:e.size+=i;break;case`shrink`:e.size-=i;break;case`left`:e.x-=i;break;case`right`:e.x+=i;break;case`up`:e.y-=i;break;case`down`:e.y+=i;break;case`rotate`:e.rotate+=i;break}return e},{size:16,x:0,y:0,flipX:!1,flipY:!1,rotate:0})},xi={mixout:function(){return{parse:{transform:function(e){return bi(e)}}}},hooks:function(){return{parseNodeAttributes:function(e,t){var n=t.getAttribute(`data-fa-transform`);return n&&(e.transform=bi(n)),e}}},provides:function(e){e.generateAbstractTransformGrouping=function(e){var t=e.main,n=e.transform,r=e.containerWidth,i=e.iconWidth,a={outer:{transform:`translate(${r/2} 256)`},inner:{transform:`${`translate(${n.x*32}, ${n.y*32}) `} ${`scale(${n.size/16*(n.flipX?-1:1)}, ${n.size/16*(n.flipY?-1:1)}) `} ${`rotate(${n.rotate} 0 0)`}`},path:{transform:`translate(${i/2*-1} -256)`}};return{tag:`g`,attributes:v({},a.outer),children:[{tag:`g`,attributes:v({},a.inner),children:[{tag:t.icon.tag,children:t.icon.children,attributes:v(v({},t.icon.attributes),a.path)}]}]}}}},Si={x:0,y:0,width:`100%`,height:`100%`};function Ci(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0;return e.attributes&&(e.attributes.fill||t)&&(e.attributes.fill=`black`),e}function wi(e){return e.tag===`g`?e.children:[e]}tr([mn,$r,ei,ti,ni,_i,yi,xi,{hooks:function(){return{parseNodeAttributes:function(e,t){var n=t.getAttribute(`data-fa-mask`),r=n?qn(n.split(` `).map(function(e){return e.trim()})):Vn();return r.prefix||=V(),e.mask=r,e.maskId=t.getAttribute(`data-fa-mask-id`),e}}},provides:function(e){e.generateAbstractMask=function(e){var t=e.children,n=e.attributes,r=e.main,i=e.mask,a=e.maskId,o=e.transform,s=r.width,c=r.icon,l=i.width,u=i.icon,d=cn({transform:o,containerWidth:l,iconWidth:s}),f={tag:`rect`,attributes:v(v({},Si),{},{fill:`white`})},p=c.children?{children:c.children.map(Ci)}:{},m={tag:`g`,attributes:v({},d.inner),children:[Ci(v({tag:c.tag,attributes:v(v({},c.attributes),d.path)},p))]},h={tag:`g`,attributes:v({},d.outer),children:[m]},g=`mask-${a||tn()}`,_=`clip-${a||tn()}`,y={tag:`mask`,attributes:v(v({},Si),{},{id:g,maskUnits:`userSpaceOnUse`,maskContentUnits:`userSpaceOnUse`}),children:[f,h]},b={tag:`defs`,children:[{tag:`clipPath`,attributes:{id:_},children:wi(u)},y]};return t.push(b,{tag:`rect`,attributes:v({fill:`currentColor`,"clip-path":`url(#${_})`,mask:`url(#${g})`},Si)}),{children:t,attributes:n}}}},{provides:function(e){var t=!1;S.matchMedia&&(t=S.matchMedia(`(prefers-reduced-motion: reduce)`).matches),e.missingIconAbstract=function(){var e=[],n={fill:`currentColor`},r={attributeType:`XML`,repeatCount:`indefinite`,dur:`2s`};e.push({tag:`path`,attributes:v(v({},n),{},{d:`M156.5,447.7l-12.6,29.5c-18.7-9.5-35.9-21.2-51.5-34.9l22.7-22.7C127.6,430.5,141.5,440,156.5,447.7z M40.6,272H8.5 c1.4,21.2,5.4,41.7,11.7,61.1L50,321.2C45.1,305.5,41.8,289,40.6,272z M40.6,240c1.4-18.8,5.2-37,11.1-54.1l-29.5-12.6 C14.7,194.3,10,216.7,8.5,240H40.6z M64.3,156.5c7.8-14.9,17.2-28.8,28.1-41.5L69.7,92.3c-13.7,15.6-25.5,32.8-34.9,51.5 L64.3,156.5z M397,419.6c-13.9,12-29.4,22.3-46.1,30.4l11.9,29.8c20.7-9.9,39.8-22.6,56.9-37.6L397,419.6z M115,92.4 c13.9-12,29.4-22.3,46.1-30.4l-11.9-29.8c-20.7,9.9-39.8,22.6-56.8,37.6L115,92.4z M447.7,355.5c-7.8,14.9-17.2,28.8-28.1,41.5 l22.7,22.7c13.7-15.6,25.5-32.9,34.9-51.5L447.7,355.5z M471.4,272c-1.4,18.8-5.2,37-11.1,54.1l29.5,12.6 c7.5-21.1,12.2-43.5,13.6-66.8H471.4z M321.2,462c-15.7,5-32.2,8.2-49.2,9.4v32.1c21.2-1.4,41.7-5.4,61.1-11.7L321.2,462z M240,471.4c-18.8-1.4-37-5.2-54.1-11.1l-12.6,29.5c21.1,7.5,43.5,12.2,66.8,13.6V471.4z M462,190.8c5,15.7,8.2,32.2,9.4,49.2h32.1 c-1.4-21.2-5.4-41.7-11.7-61.1L462,190.8z M92.4,397c-12-13.9-22.3-29.4-30.4-46.1l-29.8,11.9c9.9,20.7,22.6,39.8,37.6,56.9 L92.4,397z M272,40.6c18.8,1.4,36.9,5.2,54.1,11.1l12.6-29.5C317.7,14.7,295.3,10,272,8.5V40.6z M190.8,50 c15.7-5,32.2-8.2,49.2-9.4V8.5c-21.2,1.4-41.7,5.4-61.1,11.7L190.8,50z M442.3,92.3L419.6,115c12,13.9,22.3,29.4,30.5,46.1 l29.8-11.9C470,128.5,457.3,109.4,442.3,92.3z M397,92.4l22.7-22.7c-15.6-13.7-32.8-25.5-51.5-34.9l-12.6,29.5 C370.4,72.1,384.4,81.5,397,92.4z`})});var i=v(v({},r),{},{attributeName:`opacity`}),a={tag:`circle`,attributes:v(v({},n),{},{cx:`256`,cy:`364`,r:`28`}),children:[]};return t||a.children.push({tag:`animate`,attributes:v(v({},r),{},{attributeName:`r`,values:`28;14;28;28;14;28;`})},{tag:`animate`,attributes:v(v({},i),{},{values:`1;0;1;1;0;1;`})}),e.push(a),e.push({tag:`path`,attributes:v(v({},n),{},{opacity:`1`,d:`M263.7,312h-16c-6.6,0-12-5.4-12-12c0-71,77.4-63.9,77.4-107.8c0-20-17.8-40.2-57.4-40.2c-29.1,0-44.3,9.6-59.2,28.7 c-3.9,5-11.1,6-16.2,2.4l-13.1-9.2c-5.6-3.9-6.9-11.8-2.6-17.2c21.2-27.2,46.4-44.7,91.2-44.7c52.3,0,97.4,29.8,97.4,80.2 c0,67.6-77.4,63.5-77.4,107.8C275.7,306.6,270.3,312,263.7,312z`}),children:t?[]:[{tag:`animate`,attributes:v(v({},i),{},{values:`1;0;0;0;0;1;`})}]}),t||e.push({tag:`path`,attributes:v(v({},n),{},{opacity:`0`,d:`M232.5,134.5l7,168c0.3,6.4,5.6,11.5,12,11.5h9c6.4,0,11.7-5.1,12-11.5l7-168c0.3-6.8-5.2-12.5-12-12.5h-23 C237.7,122,232.2,127.7,232.5,134.5z`}),children:[{tag:`animate`,attributes:v(v({},i),{},{values:`0;0;1;1;0;0;`})}]}),{tag:`g`,attributes:{class:`missing`},children:e}}}},{hooks:function(){return{parseNodeAttributes:function(e,t){var n=t.getAttribute(`data-fa-symbol`);return e.symbol=n===null?!1:n===``?!0:n,e}}}}],{mixoutsTo:K}),K.noAuto;var J=K.config;K.library,K.dom;var Ti=K.parse;K.findIconDefinition,K.toHtml;var Ei=K.icon;K.layer,K.text,K.counter;var Y=e(n(),1),Di=e(t(),1);function Oi(e){return e-=0,e===e}function ki(e){return Oi(e)?e:(e=e.replace(/[_-]+(.)?/g,(e,t)=>t?t.toUpperCase():``),e.charAt(0).toLowerCase()+e.slice(1))}function Ai(e){return e.charAt(0).toUpperCase()+e.slice(1)}var X=new Map,ji=1e3;function Mi(e){if(X.has(e))return X.get(e);let t={},n=0,r=e.length;for(;n<r;){let i=e.indexOf(`;`,n),a=i===-1?r:i,o=e.slice(n,a).trim();if(o){let e=o.indexOf(`:`);if(e>0){let n=o.slice(0,e).trim(),r=o.slice(e+1).trim();if(n&&r){let e=ki(n);t[e.startsWith(`webkit`)?Ai(e):e]=r}}}n=a+1}if(X.size===ji){let e=X.keys().next().value;e&&X.delete(e)}return X.set(e,t),t}function Ni(e,t,n={}){if(typeof t==`string`)return t;let r=(t.children||[]).map(t=>Ni(e,t)),i=t.attributes||{},a={};for(let[e,t]of Object.entries(i))switch(!0){case e===`class`:a.className=t;break;case e===`style`:a.style=Mi(String(t));break;case e.startsWith(`aria-`):case e.startsWith(`data-`):a[e.toLowerCase()]=t;break;default:a[ki(e)]=t}let{style:o,role:s,"aria-label":c,...l}=n;return o&&(a.style=a.style?{...a.style,...o}:o),s&&(a.role=s),c&&(a[`aria-label`]=c,a[`aria-hidden`]=`false`),e(t.tag,{...l,...a},...r)}var Pi=Ni.bind(null,Y.createElement),Fi=(e,t)=>{let n=(0,Y.useId)();return e||(t?n:void 0)},Ii=class{constructor(e=`react-fontawesome`){this.enabled=!1;let t=!1;try{t=typeof process<`u`&&!1}catch{}this.scope=e,this.enabled=t}log(...e){this.enabled&&console.log(`[${this.scope}]`,...e)}warn(...e){this.enabled&&console.warn(`[${this.scope}]`,...e)}error(...e){this.enabled&&console.error(`[${this.scope}]`,...e)}};typeof process<`u`&&{}.FA_VERSION;var Li=`searchPseudoElementsFullScan`in J?`7.0.0`:`6.0.0`,Ri=Number.parseInt(Li)>=7,Z=`fa`,Q={beat:`fa-beat`,fade:`fa-fade`,beatFade:`fa-beat-fade`,bounce:`fa-bounce`,shake:`fa-shake`,spin:`fa-spin`,spinPulse:`fa-spin-pulse`,spinReverse:`fa-spin-reverse`,pulse:`fa-pulse`},zi={left:`fa-pull-left`,right:`fa-pull-right`},Bi={90:`fa-rotate-90`,180:`fa-rotate-180`,270:`fa-rotate-270`},Vi={"2xs":`fa-2xs`,xs:`fa-xs`,sm:`fa-sm`,lg:`fa-lg`,xl:`fa-xl`,"2xl":`fa-2xl`,"1x":`fa-1x`,"2x":`fa-2x`,"3x":`fa-3x`,"4x":`fa-4x`,"5x":`fa-5x`,"6x":`fa-6x`,"7x":`fa-7x`,"8x":`fa-8x`,"9x":`fa-9x`,"10x":`fa-10x`},$={border:`fa-border`,fixedWidth:`fa-fw`,flip:`fa-flip`,flipHorizontal:`fa-flip-horizontal`,flipVertical:`fa-flip-vertical`,inverse:`fa-inverse`,rotateBy:`fa-rotate-by`,swapOpacity:`fa-swap-opacity`,widthAuto:`fa-width-auto`},Hi={default:`fa-layers`};function Ui(e){let t=J.cssPrefix||J.familyPrefix||Z;return t===Z?e:e.replace(new RegExp(String.raw`(?<=^|\s)${Z}-`,`g`),`${t}-`)}function Wi(e){let{beat:t,fade:n,beatFade:r,bounce:i,shake:a,spin:o,spinPulse:s,spinReverse:c,pulse:l,fixedWidth:u,inverse:d,border:f,flip:p,size:m,rotation:h,pull:g,swapOpacity:_,rotateBy:v,widthAuto:y,className:b}=e,x=[];return b&&x.push(...b.split(` `)),t&&x.push(Q.beat),n&&x.push(Q.fade),r&&x.push(Q.beatFade),i&&x.push(Q.bounce),a&&x.push(Q.shake),o&&x.push(Q.spin),c&&x.push(Q.spinReverse),s&&x.push(Q.spinPulse),l&&x.push(Q.pulse),u&&x.push($.fixedWidth),d&&x.push($.inverse),f&&x.push($.border),p===!0&&x.push($.flip),(p===`horizontal`||p===`both`)&&x.push($.flipHorizontal),(p===`vertical`||p===`both`)&&x.push($.flipVertical),m!=null&&x.push(Vi[m]),h!=null&&h!==0&&x.push(Bi[h]),g!=null&&x.push(zi[g]),_&&x.push($.swapOpacity),Ri?(v&&x.push($.rotateBy),y&&x.push($.widthAuto),(J.cssPrefix||J.familyPrefix||Z)===Z?x:x.map(Ui)):x}var Gi=e=>typeof e==`object`&&`icon`in e&&!!e.icon;function Ki(e){if(e)return Gi(e)?e:Ti.icon(e)}function qi(e){return Object.keys(e)}var Ji=new Ii(`FontAwesomeIcon`),Yi={border:!1,className:``,mask:void 0,maskId:void 0,fixedWidth:!1,inverse:!1,flip:!1,icon:void 0,listItem:!1,pull:void 0,pulse:!1,rotation:void 0,rotateBy:!1,size:void 0,spin:!1,spinPulse:!1,spinReverse:!1,beat:!1,fade:!1,beatFade:!1,bounce:!1,shake:!1,symbol:!1,title:``,titleId:void 0,transform:void 0,swapOpacity:!1,widthAuto:!1},Xi=new Set(Object.keys(Yi)),Zi=Y.forwardRef((e,t)=>{let n={...Yi,...e},{icon:r,mask:i,symbol:a,title:o,titleId:s,maskId:c,transform:l}=n,u=Fi(c,!!i),d=Fi(s,!!o),f=Ki(r);if(!f)return Ji.error(`Icon lookup is undefined`,r),null;let p=Wi(n),m=typeof l==`string`?Ti.transform(l):l,h=Ki(i),g=Ei(f,{...p.length>0&&{classes:p},...m&&{transform:m},...h&&{mask:h},symbol:a,title:o,titleId:d,maskId:u});if(!g)return Ji.error(`Could not find icon`,f),null;let{abstract:_}=g,v={ref:t};for(let e of qi(n))Xi.has(e)||(v[e]=n[e]);return Pi(_[0],v)});Zi.displayName=`FontAwesomeIcon`,`${Hi.default}${$.fixedWidth}`;function Qi({variant:e=`action`,icon:t,iconClassName:n=`text-sm`,children:r,className:i=``,disabled:a,...o}){return(0,Di.jsxs)(`button`,{type:`button`,className:`flex items-center justify-center transition-all duration-50 ease-in-out rounded font-medium ${a?`cursor-not-allowed opacity-50`:`cursor-pointer`} ${{primary:`
      px-3 py-1.5 text-sm shadow-md
      bg-btn-primary dark:bg-btn-primary-dark
      text-btn-primary-text dark:text-btn-primary-text-dark
      hover:bg-btn-primary-hover dark:hover:bg-btn-primary-hover-dark
  `,secondary:`
      px-3 py-1.5 text-sm border
      bg-btn-secondary dark:bg-btn-secondary-dark
      text-btn-secondary-text dark:text-btn-secondary-text-dark
      border-btn-secondary-border dark:border-btn-secondary-border-dark
      hover:bg-btn-secondary-hover dark:hover:bg-btn-secondary-hover-dark
      hover:text-btn-secondary-text-hover dark:hover:text-btn-secondary-text-hover-dark
      hover:border-btn-secondary-border-hover dark:hover:border-btn-secondary-border-hover-dark
      active:bg-btn-secondary-active dark:active:bg-btn-secondary-active-dark
      active:text-btn-secondary-text-active dark:active:text-btn-secondary-text-active-dark
      active:border-btn-secondary-border-active dark:active:border-btn-secondary-border-active-dark
      transition-all duration-200
  `,danger:`
      px-3 py-1.5 text-sm shadow-md
      bg-btn-danger dark:bg-btn-danger-dark
      text-btn-danger-text dark:text-btn-danger-text-dark
      hover:bg-btn-danger-hover dark:hover:bg-btn-danger-hover-dark
  `,action:`
      p-1 border text-xs
      bg-btn-secondary dark:bg-btn-secondary-dark
      hover:bg-btn-secondary-hover dark:hover:bg-btn-secondary-hover-dark
      text-btn-primary dark:text-btn-primary-dark
      hover:text-btn-primary-hover dark:hover:text-btn-primary-hover-dark
      border-btn-secondary dark:border-btn-secondary-dark
      hover:border-btn-secondary-border-hover dark:hover:border-btn-secondary-border-hover-dark
  `,ghost:`
      p-1 px-2 py-2
      text-text-primary dark:text-text-primary-dark
      hover:text-text-primary-hover dark:hover:text-text-primary-hover-dark
      hover:bg-bg-primary-hover dark:hover:bg-bg-primary-hover-dark
  `}[e]} ${i}`.replace(/\s+/g,` `).trim(),disabled:a,...o,children:[t&&(0,Di.jsx)(Zi,{icon:t,className:n}),r&&(0,Di.jsx)(`span`,{className:t?`ml-1`:``,children:r})]})}var $i={prefix:`fas`,iconName:`magnifying-glass`,icon:[512,512,[128269,`search`],`f002`,`M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376C296.3 401.1 253.9 416 208 416 93.1 416 0 322.9 0 208S93.1 0 208 0 416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z`]},ea={prefix:`fas`,iconName:`trash`,icon:[448,512,[],`f1f8`,`M136.7 5.9L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-8.7-26.1C306.9-7.2 294.7-16 280.9-16L167.1-16c-13.8 0-26 8.8-30.4 21.9zM416 144L32 144 53.1 467.1C54.7 492.4 75.7 512 101 512L347 512c25.3 0 46.3-19.6 47.9-44.9L416 144z`]},ta={prefix:`fas`,iconName:`screwdriver`,icon:[576,512,[129691],`f54a`,`M352.1 146.7l0-49.6c0-10.7 5.3-20.7 14.2-26.6L485.2-8.7c6.3-4.2 14.8-3.4 20.2 2l45.4 45.5c5.4 5.4 6.2 13.8 2 20.2L473.6 177.8c-5.9 8.9-15.9 14.2-26.6 14.2l-49.6 0-90.7 90.7c15 33.3 8.9 73.9-18.5 101.3L162.1 510.1c-18.7 18.7-49.1 18.7-67.9 0L34.1 449.9c-18.7-18.7-18.7-49.1 0-67.9L160.1 256c27.4-27.4 67.9-33.6 101.3-18.5l90.7-90.7z`]},na={prefix:`fas`,iconName:`pen-to-square`,icon:[512,512,[`edit`],`f044`,`M471.6 21.7c-21.9-21.9-57.3-21.9-79.2 0L368 46.1 465.9 144 490.3 119.6c21.9-21.9 21.9-57.3 0-79.2L471.6 21.7zm-299.2 220c-6.1 6.1-10.8 13.6-13.5 21.9l-29.6 88.8c-2.9 8.6-.6 18.1 5.8 24.6s15.9 8.7 24.6 5.8l88.8-29.6c8.2-2.7 15.7-7.4 21.9-13.5L432 177.9 334.1 80 172.4 241.7zM96 64C43 64 0 107 0 160L0 416c0 53 43 96 96 96l256 0c53 0 96-43 96-96l0-96c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 96c0 17.7-14.3 32-32 32L96 448c-17.7 0-32-14.3-32-32l0-256c0-17.7 14.3-32 32-32l96 0c17.7 0 32-14.3 32-32s-14.3-32-32-32L96 64z`]},ra={prefix:`fas`,iconName:`hexagon-nodes`,icon:[448,512,[],`e699`,`M248 106.6c18.9-9 32-28.3 32-50.6c0-30.9-25.1-56-56-56s-56 25.1-56 56c0 22.3 13.1 41.6 32 50.6l0 98.8c-2.8 1.3-5.5 2.9-8 4.7l-80.1-45.8c1.6-20.8-8.6-41.6-27.9-52.8C57.2 96 23 105.2 7.5 132S1.2 193 28 208.5c1.3 .8 2.6 1.5 4 2.1l0 90.8c-1.3 .6-2.7 1.3-4 2.1C1.2 319-8 353.2 7.5 380S57.2 416 84 400.5c19.3-11.1 29.4-32 27.8-52.8l50.5-28.9c-11.5-11.2-19.9-25.6-23.8-41.7L88 306.1c-2.6-1.8-5.2-3.3-8-4.7l0-90.8c2.8-1.3 5.5-2.9 8-4.7l80.1 45.8c-.1 1.4-.2 2.8-.2 4.3c0 22.3 13.1 41.6 32 50.6l0 98.8c-18.9 9-32 28.3-32 50.6c0 30.9 25.1 56 56 56s56-25.1 56-56c0-22.3-13.1-41.6-32-50.6l0-98.8c2.8-1.3 5.5-2.9 8-4.7l80.1 45.8c-1.6 20.8 8.6 41.6 27.8 52.8c26.8 15.5 61 6.3 76.5-20.5s6.3-61-20.5-76.5c-1.3-.8-2.7-1.5-4-2.1l0-90.8c1.4-.6 2.7-1.3 4-2.1c26.8-15.5 36-49.7 20.5-76.5S390.8 96 364 111.5c-19.3 11.1-29.4 32-27.8 52.8l-50.6 28.9c11.5 11.2 19.9 25.6 23.8 41.7L360 205.9c2.6 1.8 5.2 3.3 8 4.7l0 90.8c-2.8 1.3-5.5 2.9-8 4.6l-80.1-45.8c.1-1.4 .2-2.8 .2-4.3c0-22.3-13.1-41.6-32-50.6l0-98.8z`]},ia={prefix:`fas`,iconName:`sun`,icon:[576,512,[9728],`f185`,`M178.2-10.1c7.4-3.1 15.8-2.2 22.5 2.2l87.8 58.2 87.8-58.2c6.7-4.4 15.1-5.2 22.5-2.2S411.4-.5 413 7.3l20.9 103.2 103.2 20.9c7.8 1.6 14.4 7 17.4 14.3s2.2 15.8-2.2 22.5l-58.2 87.8 58.2 87.8c4.4 6.7 5.2 15.1 2.2 22.5s-9.6 12.8-17.4 14.3L433.8 401.4 413 504.7c-1.6 7.8-7 14.4-14.3 17.4s-15.8 2.2-22.5-2.2l-87.8-58.2-87.8 58.2c-6.7 4.4-15.1 5.2-22.5 2.2s-12.8-9.6-14.3-17.4L143 401.4 39.7 380.5c-7.8-1.6-14.4-7-17.4-14.3s-2.2-15.8 2.2-22.5L82.7 256 24.5 168.2c-4.4-6.7-5.2-15.1-2.2-22.5s9.6-12.8 17.4-14.3L143 110.6 163.9 7.3c1.6-7.8 7-14.4 14.3-17.4zM207.6 256a80.4 80.4 0 1 1 160.8 0 80.4 80.4 0 1 1 -160.8 0zm208.8 0a128.4 128.4 0 1 0 -256.8 0 128.4 128.4 0 1 0 256.8 0z`]},aa={prefix:`fas`,iconName:`microscope`,icon:[512,512,[128300],`f610`,`M176 0c-26.5 0-48 21.5-48 48l0 208c0 26.5 21.5 48 48 48l64 0c26.5 0 48-21.5 48-48l0-64 32 0c70.7 0 128 57.3 128 128S390.7 448 320 448L32 448c-17.7 0-32 14.3-32 32s14.3 32 32 32l448 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-16.9 0c30.4-34 48.9-78.8 48.9-128 0-106-86-192-192-192l-32 0 0-80c0-26.5-21.5-48-48-48L176 0zM120 352c-13.3 0-24 10.7-24 24s10.7 24 24 24l176 0c13.3 0 24-10.7 24-24s-10.7-24-24-24l-176 0z`]},oa={prefix:`fas`,iconName:`circle-exclamation`,icon:[512,512,[`exclamation-circle`],`f06a`,`M256 512a256 256 0 1 1 0-512 256 256 0 1 1 0 512zm0-192a32 32 0 1 0 0 64 32 32 0 1 0 0-64zm0-192c-18.2 0-32.7 15.5-31.4 33.7l7.4 104c.9 12.6 11.4 22.3 23.9 22.3 12.6 0 23-9.7 23.9-22.3l7.4-104c1.3-18.2-13.1-33.7-31.4-33.7z`]},sa={prefix:`fas`,iconName:`user-group`,icon:[576,512,[128101,`user-friends`],`f500`,`M64 128a112 112 0 1 1 224 0 112 112 0 1 1 -224 0zM0 464c0-97.2 78.8-176 176-176s176 78.8 176 176l0 6c0 23.2-18.8 42-42 42L42 512c-23.2 0-42-18.8-42-42l0-6zM432 64a96 96 0 1 1 0 192 96 96 0 1 1 0-192zm0 240c79.5 0 144 64.5 144 144l0 22.4c0 23-18.6 41.6-41.6 41.6l-144.8 0c6.6-12.5 10.4-26.8 10.4-42l0-6c0-51.5-17.4-98.9-46.5-136.7 22.6-14.7 49.6-23.3 78.5-23.3z`]},ca={prefix:`fas`,iconName:`wrench`,icon:[576,512,[128295],`f0ad`,`M509.4 98.6c7.6-7.6 20.3-5.7 24.1 4.3 6.8 17.7 10.5 37 10.5 57.1 0 88.4-71.6 160-160 160-17.5 0-34.4-2.8-50.2-8L146.9 498.9c-28.1 28.1-73.7 28.1-101.8 0s-28.1-73.7 0-101.8L232 210.2c-5.2-15.8-8-32.6-8-50.2 0-88.4 71.6-160 160-160 20.1 0 39.4 3.7 57.1 10.5 10 3.8 11.8 16.5 4.3 24.1l-88.7 88.7c-3 3-4.7 7.1-4.7 11.3l0 41.4c0 8.8 7.2 16 16 16l41.4 0c4.2 0 8.3-1.7 11.3-4.7l88.7-88.7z`]},la={prefix:`fas`,iconName:`user`,icon:[448,512,[128100,62144,62470,`user-alt`,`user-large`],`f007`,`M224 248a120 120 0 1 0 0-240 120 120 0 1 0 0 240zm-29.7 56C95.8 304 16 383.8 16 482.3 16 498.7 29.3 512 45.7 512l356.6 0c16.4 0 29.7-13.3 29.7-29.7 0-98.5-79.8-178.3-178.3-178.3l-59.4 0z`]},ua={prefix:`fas`,iconName:`xmark`,icon:[384,512,[128473,10005,10006,10060,215,`close`,`multiply`,`remove`,`times`],`f00d`,`M55.1 73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L147.2 256 9.9 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192.5 301.3 329.9 438.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.8 256 375.1 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192.5 210.7 55.1 73.4z`]},da=ua,fa={prefix:`fas`,iconName:`circle-check`,icon:[512,512,[61533,`check-circle`],`f058`,`M256 512a256 256 0 1 1 0-512 256 256 0 1 1 0 512zM374 145.7c-10.7-7.8-25.7-5.4-33.5 5.3L221.1 315.2 169 263.1c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l72 72c5 5 11.8 7.5 18.8 7s13.4-4.1 17.5-9.8L379.3 179.2c7.8-10.7 5.4-25.7-5.3-33.5z`]},pa={prefix:`fas`,iconName:`moon`,icon:[512,512,[127769,9214],`f186`,`M256 0C114.6 0 0 114.6 0 256S114.6 512 256 512c68.8 0 131.3-27.2 177.3-71.4 7.3-7 9.4-17.9 5.3-27.1s-13.7-14.9-23.8-14.1c-4.9 .4-9.8 .6-14.8 .6-101.6 0-184-82.4-184-184 0-72.1 41.5-134.6 102.1-164.8 9.1-4.5 14.3-14.3 13.1-24.4S322.6 8.5 312.7 6.3C294.4 2.2 275.4 0 256 0z`]},ma={prefix:`fas`,iconName:`triangle-exclamation`,icon:[512,512,[9888,`exclamation-triangle`,`warning`],`f071`,`M256 0c14.7 0 28.2 8.1 35.2 21l216 400c6.7 12.4 6.4 27.4-.8 39.5S486.1 480 472 480L40 480c-14.1 0-27.2-7.4-34.4-19.5s-7.5-27.1-.8-39.5l216-400c7-12.9 20.5-21 35.2-21zm0 352a32 32 0 1 0 0 64 32 32 0 1 0 0-64zm0-192c-18.2 0-32.7 15.5-31.4 33.7l7.4 104c.9 12.5 11.4 22.3 23.9 22.3 12.6 0 23-9.7 23.9-22.3l7.4-104c1.3-18.2-13.1-33.7-31.4-33.7z`]},ha={prefix:`fas`,iconName:`lock`,icon:[384,512,[128274],`f023`,`M128 96l0 64 128 0 0-64c0-35.3-28.7-64-64-64s-64 28.7-64 64zM64 160l0-64C64 25.3 121.3-32 192-32S320 25.3 320 96l0 64c35.3 0 64 28.7 64 64l0 224c0 35.3-28.7 64-64 64L64 512c-35.3 0-64-28.7-64-64L0 224c0-35.3 28.7-64 64-64z`]},ga={prefix:`fas`,iconName:`plus`,icon:[448,512,[10133,61543,`add`],`2b`,`M256 64c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 160-160 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l160 0 0 160c0 17.7 14.3 32 32 32s32-14.3 32-32l0-160 160 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-160 0 0-160z`]},_a={prefix:`fas`,iconName:`copy`,icon:[448,512,[],`f0c5`,`M192 0c-35.3 0-64 28.7-64 64l0 256c0 35.3 28.7 64 64 64l192 0c35.3 0 64-28.7 64-64l0-200.6c0-17.4-7.1-34.1-19.7-46.2L370.6 17.8C358.7 6.4 342.8 0 326.3 0L192 0zM64 128c-35.3 0-64 28.7-64 64L0 448c0 35.3 28.7 64 64 64l192 0c35.3 0 64-28.7 64-64l0-16-64 0 0 16-192 0 0-256 16 0 0-64-16 0z`]},va={prefix:`fas`,iconName:`bars`,icon:[448,512,[`navicon`],`f0c9`,`M0 96C0 78.3 14.3 64 32 64l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 128C14.3 128 0 113.7 0 96zM0 256c0-17.7 14.3-32 32-32l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 288c-17.7 0-32-14.3-32-32zM448 416c0 17.7-14.3 32-32 32L32 448c-17.7 0-32-14.3-32-32s14.3-32 32-32l384 0c17.7 0 32 14.3 32 32z`]},ya={prefix:`fas`,iconName:`angles-left`,icon:[448,512,[171,`angle-double-left`],`f100`,`M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L77.3 256 214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L269.3 256 406.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z`]},ba={prefix:`fas`,iconName:`square-share-nodes`,icon:[448,512,[`share-alt-square`],`f1e1`,`M64 32C28.7 32 0 60.7 0 96L0 416c0 35.3 28.7 64 64 64l320 0c35.3 0 64-28.7 64-64l0-320c0-35.3-28.7-64-64-64L64 32zM368 160c0 35.3-28.7 64-64 64-15.4 0-29.5-5.4-40.6-14.5l-85.3 46.5 85.3 46.5c11-9.1 25.2-14.5 40.6-14.5 35.3 0 64 28.7 64 64s-28.7 64-64 64-64-28.7-64-64c0-2.5 .1-4.9 .4-7.3L158.5 300c-11.7 12.3-28.2 20-46.5 20-35.3 0-64-28.7-64-64s28.7-64 64-64c18.3 0 34.8 7.7 46.5 20l81.9-44.7c-.3-2.4-.4-4.9-.4-7.3 0-35.3 28.7-64 64-64s64 28.7 64 64z`]},xa={prefix:`fas`,iconName:`circle-info`,icon:[512,512,[`info-circle`],`f05a`,`M256 512a256 256 0 1 0 0-512 256 256 0 1 0 0 512zM224 160a32 32 0 1 1 64 0 32 32 0 1 1 -64 0zm-8 64l48 0c13.3 0 24 10.7 24 24l0 88 8 0c13.3 0 24 10.7 24 24s-10.7 24-24 24l-80 0c-13.3 0-24-10.7-24-24s10.7-24 24-24l24 0 0-64-24 0c-13.3 0-24-10.7-24-24s10.7-24 24-24z`]},Sa=null,Ca=null;function wa(e){if(Sa)return Promise.resolve(Sa);if(window.__RUNTIME_CONFIG__)return Sa=window.__RUNTIME_CONFIG__,Promise.resolve(Sa);if(Ca)return Ca;let t=new URL(`../config.json`,``+import.meta.url).toString();return Ca=fetch(t,{cache:`no-store`,signal:e}).then(async e=>{if(!e.ok)throw Error(`Failed to load config.json: ${e.status} ${e.statusText}`);let t=await e.json();return Sa=t,t}).finally(()=>{Ca=null}),Ca}const Ta={ALL_GROUPS:`/api/2.0/mlflow/permissions/groups`,ALL_EXPERIMENTS:`/api/2.0/mlflow/permissions/experiments`,ALL_MODELS:`/api/2.0/mlflow/permissions/registered-models`,ALL_PROMPTS:`/api/2.0/mlflow/permissions/prompts`,CREATE_ACCESS_TOKEN:`/api/2.0/mlflow/users/access-token`,GET_CURRENT_USER:`/api/2.0/mlflow/users/current`,USERS_RESOURCE:`/api/2.0/mlflow/users`},Ea={GET_USER_DETAILS:e=>`/api/2.0/mlflow/users/${e}`,USER_EXPERIMENT_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/users/${e}/experiments`,USER_EXPERIMENT_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/users/${e}/experiments/${t}`,USER_MODEL_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/users/${e}/registered-models`,USER_MODEL_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/users/${e}/registered-models/${t}`,USER_PROMPT_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/users/${e}/prompts`,USER_PROMPT_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/users/${e}/prompts/${t}`,USER_EXPERIMENT_PATTERN_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/users/${e}/experiment-patterns`,USER_EXPERIMENT_PATTERN_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/users/${e}/experiment-patterns/${t}`,USER_MODEL_PATTERN_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/users/${e}/registered-models-patterns`,USER_MODEL_PATTERN_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/users/${e}/registered-models-patterns/${t}`,USER_PROMPT_PATTERN_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/users/${e}/prompts-patterns`,USER_PROMPT_PATTERN_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/users/${e}/prompts-patterns/${t}`,EXPERIMENT_USER_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/experiments/${encodeURIComponent(String(e))}/users`,MODEL_USER_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/registered-models/${encodeURIComponent(String(e))}/users`,PROMPT_USER_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/prompts/${encodeURIComponent(String(e))}/users`,GROUP_EXPERIMENT_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/groups/${e}/experiments`,GROUP_EXPERIMENT_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/groups/${e}/experiments/${t}`,GROUP_MODEL_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/groups/${e}/registered-models`,GROUP_MODEL_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/groups/${e}/registered-models/${t}`,GROUP_PROMPT_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/groups/${e}/prompts`,GROUP_PROMPT_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/groups/${e}/prompts/${t}`,GROUP_EXPERIMENT_PATTERN_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/groups/${e}/experiment-patterns`,GROUP_EXPERIMENT_PATTERN_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/groups/${e}/experiment-patterns/${t}`,GROUP_MODEL_PATTERN_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/groups/${e}/registered-models-patterns`,GROUP_MODEL_PATTERN_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/groups/${e}/registered-models-patterns/${t}`,GROUP_PROMPT_PATTERN_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/groups/${e}/prompts-patterns`,GROUP_PROMPT_PATTERN_PERMISSION:(e,t)=>`/api/2.0/mlflow/permissions/groups/${e}/prompts-patterns/${t}`,EXPERIMENT_GROUP_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/experiments/${encodeURIComponent(String(e))}/groups`,MODEL_GROUP_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/registered-models/${encodeURIComponent(String(e))}/groups`,PROMPT_GROUP_PERMISSIONS:e=>`/api/2.0/mlflow/permissions/prompts/${encodeURIComponent(String(e))}/groups`};function Da(e){let t=new URLSearchParams;for(let[n,r]of Object.entries(e))r!=null&&t.append(n,String(r));let n=t.toString();return n?`?${n}`:``}async function Oa(e,t,n){return`${(await wa(n)).basePath}${e}${Da(t)}`}var ka=(e,t)=>{if(!t)return e;let n=new URL(e,window.location.origin);return Object.entries(t).forEach(([e,t])=>n.searchParams.set(e,t)),n.toString()};async function Aa(e,t={}){let{params:n,...r}=t,i=await fetch(ka(e,n),{...r,headers:{"Content-Type":`application/json`,...r.headers||{}},credentials:`include`});if(!i.ok){let e=await i.text();throw Error(`HTTP ${i.status}: ${e}`)}return(i.headers.get(`content-type`)||``).includes(`application/json`)?await i.json():await i.text()}function ja({endpointKey:e,queryParams:t={},headers:n={}}){let r=Ta[e];return async function(e){return Aa(await Oa(r,t,e),{method:`GET`,signal:e,headers:{...n}})}}function Ma({endpointKey:e,queryParams:t={},headers:n={}}){let r=Ea[e];return async function(...e){let i=e.slice(0,r.length),a=e[r.length];return Aa(await Oa(r(...i),t,a),{method:`GET`,signal:a,headers:{...n}})}}function Na(e){let[t,n]=(0,Y.useState)(null),[r,a]=(0,Y.useState)(!1),[o,s]=(0,Y.useState)(null),{isAuthenticated:c}=i(),l=(0,Y.useCallback)(e,[e]);return(0,Y.useEffect)(()=>{if(c){let e=new AbortController,t=!1;return(async()=>{a(!0),s(null);try{let r=await l(e.signal);t||n(r)}catch(e){t||(s(e instanceof Error?e:Error(String(e))),n(null))}finally{t||a(!1)}})(),()=>{t=!0,e.abort()}}},[c,l]),{data:t,isLoading:r,error:o,refetch:(0,Y.useCallback)(()=>{a(!0),s(null);let t=new AbortController;e(t.signal).then(e=>{n(e)}).catch(e=>{t.signal.aborted||(s(e instanceof Error?e:Error(String(e))),n(null))}).finally(()=>{a(!1)})},[e])}}export{ua as A,ba as C,la as D,ea as E,Zi as M,i as N,sa as O,$i as S,da as T,ha as _,Ea as a,ga as b,ya as c,_a as d,na as f,xa as g,ra as h,Aa as i,Qi as j,ca as k,va as l,ma as m,Ma as n,Ta as o,oa as p,ja as r,wa as s,Na as t,fa as u,aa as v,ia as w,ta as x,pa as y};