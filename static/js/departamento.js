
var xobj = new XMLHttpRequest();
xobj.open('GET', '/static/js/departamentos.json', false);
xobj.send(null);
var x = JSON.parse(xobj.responseText);
var h = '';
for(var i=0; i<32; i=i+1){
	h = h +'<option value="'+x[i]["departamento"]+'">'+x[i]["departamento"]+'</option>';
}
document.getElementById("departamento").innerHTML = h;

function muni(){
	var depar = document.getElementById("departamento");
	//document.write(depar.value);
    var index = 0;
    for (var i = 0; i<32; i +=1){
    	if (x[i]["departamento"] == depar.value){
        	index = i;
        }
    }
    var m = '<option selected="true" disabled="disabled">seleccione...</option>';
    ciud = x[index]["ciudades"];
    for(var v in ciud){
		m = m +'<option value="'+ciud[v]+'">'+ciud[v]+'</option>';
	}
    document.getElementById("municipio").innerHTML = m;
}
