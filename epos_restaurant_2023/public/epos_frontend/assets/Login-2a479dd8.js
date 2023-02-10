var x=(y,v,m)=>new Promise((o,u)=>{var l=n=>{try{g(m.next(n))}catch(f){u(f)}},k=n=>{try{g(m.throw(n))}catch(f){u(f)}},g=n=>n.done?o(n.value):Promise.resolve(n.value).then(l,k);g((m=m.apply(y,v)).next())});import{_ as P,u as j,r as A,a as O,c as L,i as D,b as E,w as i,d as p,o as J,e as t,f as e,g as a,t as h,n as R,h as U,j as c,k as z,A as H}from"./index-c67f2058.js";const M={class:"h-full w-full p-10 flex justify-center items-center"},T={class:"app-info w-96 inline-block text-center rounded-lg pa-4 bg-gradient-to-t from-yellow-900 to-yellow-700 text-white shadow-sm"},q={class:"mb-3"},F=["src"],G={class:"font-bold mb-3"},K={class:"py-3"},Q={class:"h-full flex items-center justify-center bg-gray-100"},W=["onSubmit"],X={class:"w-73"},Y={class:"d-block d-md-none mt-4"},Z={class:"mb-3"},ss=["src"],es={class:"text-center mb-3"},ts={class:"font-bold mb-1 text-2xl"},os={class:"text-sm"},ns={class:"mb-3"},is={class:"relative"},as={class:"grid grid-cols-3 gap-3"},ls={class:"mt-6"},rs={class:"mt-4 text-center"},ds={class:"text-sm text-green-700"},cs={__name:"Login",setup(y){const v=H(),m=j();let o=A({username:"",password:""});const u=O(),l=L(()=>JSON.parse(localStorage.getItem("setting"))),k=L(()=>u.state.isLoading),g=D("$auth");u.state.isLoading=!1;function n(b){o.password==null&&(o.password=""),o.password=o.password+b}function f(){o.password=""}function S(){o.password=o.password.substring(0,o.password.length-1)}const $=()=>x(this,null,function*(){if(!o.password){v.warning("Invalid Password",{position:"top"});return}u.dispatch("startLoading"),z({url:"epos_restaurant_2023.api.api.check_username",auto:!0,params:{pin_code:o.password},onSuccess(s){return x(this,null,function*(){u.dispatch("startLoading"),o.username=s.username,o.username&&o.password&&((yield g.login(o.username,o.password))?I(s):(v.warning("Login fail. Invalid username or password."),u.dispatch("endLoading")))})},onError(s){u.dispatch("endLoading")}})});function I(b){z({url:"epos_restaurant_2023.api.api.get_user_information",auto:!0,onSuccess(_){return x(this,null,function*(){_.permission=b.permission,localStorage.setItem("current_user",JSON.stringify(_)),m.push({name:"Home"}),u.dispatch("endLoading")})},onError(_){u.dispatch("endLoading")}})}return(b,s)=>{const _=p("v-divider"),w=p("v-list-item"),N=p("v-list"),C=p("v-col"),V=p("v-text-field"),r=p("v-btn"),B=p("v-row");return J(),E(B,{class:"mt-0 mb-0 h-screen"},{default:i(()=>[t(C,{md:"8",class:"pa-0 d-sm-none d-none d-md-block"},{default:i(()=>[e("div",{class:"h-screen bg-cover bg-no-repeat bg-center",style:R({"background-image":"url("+a(l).login_background+")"})},[e("div",M,[e("div",null,[e("div",T,[e("div",q,[e("img",{class:"my-0 mx-auto",src:a(l).logo},null,8,F)]),e("h1",G,h(a(l).app_name),1),t(_),e("div",K,[t(N,{lines:"one","bg-color":"transparent"},{default:i(()=>[t(w,{class:"mb-2",title:a(l).business_branch,subtitle:"Business"},null,8,["title"]),t(w,{class:"mb-2",title:a(l).pos_profile,subtitle:"POS Profile"},null,8,["title"]),t(w,{class:"mb-2",title:a(l).phone_number,subtitle:"Phone Number"},null,8,["title"]),t(w,{title:a(l).address,subtitle:"Address"},null,8,["title"])]),_:1})])])])])],4)]),_:1}),t(C,{sm:"12",md:"4",class:"pa-0"},{default:i(()=>[e("div",Q,[e("form",{onSubmit:U($,["prevent"])},[e("div",X,[e("div",null,[e("div",Y,[e("div",Z,[e("img",{class:"my-0 mx-auto w-16",src:a(l).logo},null,8,ss)]),e("div",es,[e("h1",ts,h(a(l).app_name),1),e("p",os,h(a(l).business_branch),1),t(_)])]),e("div",ns,[e("div",is,[t(V,{type:"password",density:"compact",variant:"solo",label:"Password","append-inner-icon":"mdi-arrow-left","single-line":"","hide-details":"",modelValue:a(o).password,"onUpdate:modelValue":s[0]||(s[0]=d=>a(o).password=d),height:"200","onClick:appendInner":s[1]||(s[1]=d=>S())},null,8,["modelValue"])])]),e("div",null,[e("div",as,[t(r,{onClick:s[2]||(s[2]=d=>n("1")),size:"x-large"},{default:i(()=>[c(" 1 ")]),_:1}),t(r,{onClick:s[3]||(s[3]=d=>n("2")),size:"x-large"},{default:i(()=>[c(" 2 ")]),_:1}),t(r,{onClick:s[4]||(s[4]=d=>n("3")),size:"x-large"},{default:i(()=>[c(" 3 ")]),_:1}),t(r,{onClick:s[5]||(s[5]=d=>n("4")),size:"x-large"},{default:i(()=>[c(" 4 ")]),_:1}),t(r,{onClick:s[6]||(s[6]=d=>n("5")),size:"x-large"},{default:i(()=>[c(" 5 ")]),_:1}),t(r,{onClick:s[7]||(s[7]=d=>n("6")),size:"x-large"},{default:i(()=>[c(" 6 ")]),_:1}),t(r,{onClick:s[8]||(s[8]=d=>n("7")),size:"x-large"},{default:i(()=>[c(" 7 ")]),_:1}),t(r,{onClick:s[9]||(s[9]=d=>n("8")),size:"x-large"},{default:i(()=>[c(" 8 ")]),_:1}),t(r,{onClick:s[10]||(s[10]=d=>n("9")),size:"x-large"},{default:i(()=>[c(" 9 ")]),_:1}),t(r,{onClick:s[11]||(s[11]=d=>n("0")),size:"x-large"},{default:i(()=>[c(" 0 ")]),_:1}),t(r,{class:"col-span-2",color:"error",onClick:f,size:"x-large"},{default:i(()=>[c(" Clear ")]),_:1})])]),e("div",ls,[t(r,{type:"submit",loading:a(k),size:"x-large",class:"w-full",color:"primary"},{default:i(()=>[c("Login")]),_:1},8,["loading"])]),e("div",rs,[e("p",ds,h(a(l).pos_profile),1)])])])],40,W)])]),_:1})]),_:1})}}},ps=P(cs,[["__scopeId","data-v-0e33a683"]]);export{ps as default};