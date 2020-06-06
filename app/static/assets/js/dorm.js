var data_table
console.log("dorm js")
function create_dorm() {
    console.log("create post is working!"); // sanity check

    jQuery.support.cors = true;
    $.ajax({
      url: "http://127.0.0.1:5000/dorm", // the endpoint
      type: "POST", // http method
      data: { the_post: $("#post-text").val() }, // data sent with the post request

      // handle a successful response
      success: function(json) {
        $("#post-text").val(""); // remove the value from the input
        console.log(json); // log the returned json to the console
		data_table= json;
        //label = json.label;
        //data1 = json.data;
        //  setTimeout(create_post_Attentiveness, 1000);
        console.log("success"); // another sanity check

	var i=0
	// $('#medchange').each(function() {
		
	// 		$(this).remove();
		
  // });
  outbreak=data_table['outbreak']

  var progress_color =['progress-bar bg-warning','progress-bar bg-success','progress-bar bg-danger','progress-bar bg-info'];
 var total_tom=parseInt(outbreak['tomorrow'][0]+outbreak['tomorrow'][1]+outbreak['tomorrow'][2])
 var total_tod=parseInt(outbreak['today'][0]+outbreak['today'][1]+outbreak['today'][2])



increase_percent=['text-danger mr-2','fas fa-arrow-up']
decrease_percent=['text-success mr-2','fas fa-arrow-down']

console.log()
if (total_tom<total_tod)
  {
    var percent = parseInt((total_tod-total_tom)*100/total_tod)
    $('#ob_lm_cn').append('<span class="'+decrease_percent[0]+'"><i class="'+decrease_percent[1]+'"></i>'+percent+'%</span> <span class="text-nowrap">Since last month</span>')

  }
else if(total_tom >total_tod)
{
    var percent = parseInt((total_tom-total_tod)*100/total_tom)
    console.log('per',percent, outbreak['to'])
    $('#ob_lm_cn').append('<span class="'+increase_percent[0]+'"><i class="'+increase_percent[1]+'"></i>'+percent+'%</span> <span class="text-nowrap">Tomorrow</span>')

}
else
{
  $('#ob_l_cn').append('<span class="'+increase_percent[0]+'"><i class="'+increase_percent[1]+'"></i>0%</span> <span class="text-nowrap">Tomorrow</span>')

}

if (outbreak['tomorrow'][0]<outbreak['today'][0])
  {
    var percent = parseInt((outbreak['today'][0]-outbreak['tomorrow'][0])*100/outbreak['today'][0])
    $('#ob_lm').append('<span class="'+decrease_percent[0]+'"><i class="'+decrease_percent[1]+'"></i>'+percent+'%</span> <span class="text-nowrap">Since last month</span>')

  }
else if(outbreak['today']< outbreak['tomorrow'])
{
    var percent = parseInt((outbreak['tomorrow'][0]-outbreak['today'][0])*100/outbreak['tomorrow'][0])
    console.log('per',percent, outbreak['to'])
    $('#ob_lm').append('<span class="'+increase_percent[0]+'"><i class="'+increase_percent[1]+'"></i>'+percent+'%</span> <span class="text-nowrap">Tomorrow</span>')

}
else
{
  $('#ob_lm').append('<span class="'+increase_percent[0]+'"><i class="'+increase_percent[1]+'"></i>0%</span> <span class="text-nowrap">Since last month</span>')

}

$('#ob_tom').append(parseInt(outbreak['tomorrow'][0]))
$('#ob_con').append(parseInt(outbreak['tomorrow'][0]+outbreak['tomorrow'][1]+outbreak['tomorrow'][2]))
      },

      // handle a non-successful response
      error: function(xhr, errmsg, err) {
        $("#results").html(
          "<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " +
            errmsg +
            " <a href='#' class='close'>&times;</a></div>"
        ); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  }
  create_dorm();
function dorm_table()
{
  increase_percent=['text-danger mr-2','fas fa-arrow-up']
decrease_percent=['text-success mr-2','fas fa-arrow-down']
  var progress_color =['progress-bar bg-warning','progress-bar bg-success','progress-bar bg-danger','progress-bar bg-info'];
   var nop = parseInt($('#nocvp').val())
   var crp = parseInt($('#nocver').val())

  $('#ob-form').html('<div class="table-responsive"><table class="table align-items-center table-dark table-flush"><thead class="thead-dark"><tr><th scope="col">Resource</th><th scope="col">Total</th><th scope="col">Current </th><th scope="col">Predicted Requirement </th><th scope="col">Availability Percentage </th><th scope="col"></th></tr></thead><tbody id ="tableob"></tbody></table></div>');
  hospital = data_table['hospitalinfo']
  outbreak=data_table['outbreak']
  
  var patpercent= parseInt((nop)*100/outbreak['today'][0])
  
  
  var dif= outbreak['tomorrow'][0]-outbreak['today'][0]  
  var npat=  parseInt(dif*patpercent/100)
  console.log('pat',patpercent,dif,npat)
  var crpercent= parseInt((nop-crp)*100/nop)
  var crinc= parseInt((npat)*crpercent/100);
  var data= {'beds':[nop, nop+npat], 'doctors':[10,10],"emergency":[crp, crp+crinc],'nurses':[64,64]}
  var percentage={};
  if ((nop+npat)>hospital['beds'])
  {
    percentage['beds']=parseInt((hospital['beds'])*100/(nop+npat))
  }
  else {
        percentage['beds']=100
    }
    percentage ['doctors']=100
    percentage['nurses']=100
    if ((crp+crinc)>hospital['emergency'])
  {
    percentage['emergency']=parseInt((hospital['emergency'])*100/(crp + crinc))
  }
  else {
        percentage['emergency']=100
    }
  
var total_per=0
var i=0
  $.each( hospital,function(key,value){
      var pc = progress_color[0]
      var perc=percentage[key]
      total_per+=perc
      i=i+1
      if (perc<50)
      pc=progress_color[2]
    else if(perc<80)
      pc=progress_color[0]
    else if(perc==100)
      pc=progress_color[1]
    else 
      pc = progress_color[3]
    console.log('beds',data[key][1])
    if(data[key][1]>data[key][0])
      $('#tableob').append('<tr> <th scope="row"><div class="media align-items-center"><a href="#" class="avatar rounded-circle mr-3"><img alt="Image placeholder" src="/static/assets/img/theme/medicine-logo.jpg"></a><div class="media-body"><span class="mb-0 text-sm">'+key+'</span></div></div></th><td><span class="mb-0 text-sm">'+value+'</span></td><td>'+data[key][0]+'</td><td><span class="'+increase_percent[0]+'"><i class="'+increase_percent[1]+'"></i>'+data[key][1]+'</span></td><td><div class="d-flex align-items-center"><span class="mr-2">'+perc+'%</span><div><div class="progress"><div class="'+pc+'" role="progressbar" aria-valuenow="'+perc+'" aria-valuemin="0" aria-valuemax="100" style="width: '+perc+'%;"></div></div></div></div></td></tr>');
    else
    $('#tableob').append('<tr> <th scope="row"><div class="media align-items-center"><a href="#" class="avatar rounded-circle mr-3"><img alt="Image placeholder" src="/static/assets/img/theme/medicine-logo.jpg"></a><div class="media-body"><span class="mb-0 text-sm">'+key+'</span></div></div></th><td><span class="mb-0 text-sm">'+value+'</span></td><td>'+data[key][0]+'</td><td><span class="'+decrease_percent[0]+'"><i class="'+decrease_percent[1]+'"></i>'+data[key][1]+'</span></td><td><div class="d-flex align-items-center"><span class="mr-2">'+perc+'%</span><div><div class="progress"><div class="'+pc+'" role="progressbar" aria-valuenow="'+perc+'" aria-valuemin="0" aria-valuemax="100" style="width: '+perc+'%;"></div></div></div></div></td></tr>');

    
  })
total_per=total_per/i;
$('#ob_rc').append(parseInt(total_per)+'%')
}




