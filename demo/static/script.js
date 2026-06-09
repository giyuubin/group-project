function previewFile(){

let file=
document.getElementById(
"fileInput"
).files[0];


if(!file)return;


let size=
(
file.size/
1024/
1024
)
.toFixed(2);


document.getElementById(
"uploadContent"
).innerHTML=`

<div class="selected">

<div class="file-icon">

✅

</div>


<h2>

${file.name}

</h2>


<p>

파일 준비 완료

</p>


<p>

크기:
${size}MB

</p>


</div>

`;

}



async function uploadFile(){


let file=

document.getElementById(
"fileInput"
).files[0];


if(!file){

alert(
"파일 선택"
);

return;

}


let formData=
new FormData();


formData.append(
"file",
file
);


document.getElementById(
"result"
).innerHTML=`

<h2>

분석중...

</h2>

`;


let response=
await fetch(
"/upload",
{
method:"POST",
body:formData
}
);


let data=
await response.json();


let icon=
data.prediction
==="악성파일"

?

"⚠️"

:

"✅";


let statusClass=
data.prediction
==="악성파일"

?

"danger"

:

"safe";


document.getElementById(
"result"
).innerHTML=`

<div class=
"result-card">


<div class=
"result-icon">

${icon}

</div>


<div class=
"result-text">


<div class=
"status ${statusClass}">

${data.prediction}

</div>


<div class=
"confidence">

신뢰도:
${data.confidence}%

</div>


</div>


</div>

`;

}