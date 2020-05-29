var data_table
console.log("table js")
function create_table() {
    console.log("create post is working!"); // sanity check

    jQuery.support.cors = true;
    $.ajax({
      url: "http://127.0.0.1:5000/currenttable", // the endpoint
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
	console.log("data1",data_table['data'][0])
	var i=0
	// $('#medchange').each(function() {
		
	// 		$(this).remove();
		
  // });

  var progress_color =['progress-bar bg-warning','progress-bar bg-success','progress-bar bg-danger','progress-bar bg-info'];
 var total_usage=0
  data_table['names'].forEach((med)=>{
    var pc
    if (data_table['percentages'][i]<50)
      pc=progress_color[2]
    else if(data_table['percentages'][i]<80)
      pc=progress_color[0]
    else if(data_table['percentages'][i]==100)
      pc=progress_color[1]
    else 
      pc = progress_color[3]
  $('#table1').append('<tr> <th scope="row"><div class="media align-items-center"><a href="#" class="avatar rounded-circle mr-3"><img alt="Image placeholder" src="/static/assets/img/theme/medicine-logo.jpg"></a><div class="media-body"><span class="mb-0 text-sm">'+med+'</span></div></div></th><td><span class="mb-0 text-sm">'+data_table['data'][i]+'</span></td><td>'+data_table['nextmonth'][i]+'</td><td><div class="d-flex align-items-center"><span class="mr-2">'+data_table['percentages'][i]+'%</span><div><div class="progress"><div class="'+pc+'" role="progressbar" aria-valuenow="'+data_table['percentages'][i]+'" aria-valuemin="0" aria-valuemax="100" style="width: '+data_table['percentages'][i]+'%;"></div></div></div></div></td></tr>');

  total_usage+=parseInt(data_table['data'][i])
  i=i+1;
});
increase_percent=['text-success mr-2','fas fa-arrow-up']
decrease_percent=['text-danger mr-2','fas fa-arrow-down']

console.log()
if (total_usage<data_table['last_month'])
  {
    var percent = parseInt((data_table['last_month']-total_usage)*100/data_table['last_month'])
    $('#med_usage_lm').append('<span class="'+decrease_percent[0]+'"><i class="'+decrease_percent[1]+'"></i>'+percent+'%</span> <span class="text-nowrap">Since last month</span>')

  }
else if(total_usage > data_table['last_month'])
{
  var percent = parseFloat((total_usage-data_table['last_month'])*100/total_usage)
    $('#med_usage_lm').append('<span class="'+increase_percent[0]+'"><i class="'+increase_percent[1]+'"></i>'+percent+'%</span> <span class="text-nowrap">Since last month</span>')

}
else
{
  $('#med_usage_lm').append('<span class="'+increase_percent[0]+'"><i class="'+increase_percent[1]+'"></i>0%</span> <span class="text-nowrap">Since last month</span>')

}
$('#med_usage').append(total_usage)

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
  create_table();