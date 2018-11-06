function enable_iframe()
{
    if(rich_test.document.designMode == "on")
        return
    else
        rich_test.document.designMode = "on";
}
function change(command)
{
    rich_test.document.execCommand(command,false,null);
}
function changewitharg(command,arg)
{
    rich_test.document.execCommand(command,false,arg);
}
function show()
{
//   var x = document.getElementsByName("rich_test");
  var y = (window.frames[0].document.body.innerHTML );
  title=document.getElementById('title').value;
  alert(y);
  var formData = new FormData();
  formData.append('data', y);
  formData.append('title',title);

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    document.getElementById("new_content").innerHTML = this.responseText;
    }
};
  xhr.open('POST', 'http://127.0.0.1:5000/addrec', true);
  xhr.send(formData);
//   document.getElementById('text_name').value=y;
  return y;
}
setTimeout(enable_iframe(),50)