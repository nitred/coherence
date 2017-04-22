function clickEvent(id){
  $(id).click(function(){
    $.ajax({
      type: "POST",
      url: "http://139.59.24.127:8080/api/clickEvent",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({"click":id}),
      success: function(data){console.log(data);},
      dataType: "json"
    });
  })
}

function registerUserAndCookie(button_id, input_id){
  $(button_id).click(function(){
    $(button_id).prop('disabled', true);
    name = $(input_id).val();
    cookie_id = Cookies.getJSON("coherence")['cookie_id'];
    console.log("Registering", cookie_id, name)
    $.ajax({
      type: "POST",
      url: "http://139.59.24.127:8080/api/registerUserAndCookie",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({"name":name, "cookie_id": cookie_id}),
      success: function(data){
        console.log(data);
        Cookies.set("coherence", {"cookie_id": cookie_id, "name": name})
        setTimeout(function(){
          window.location.href = "http://139.59.24.127:8080/page1.html";
        }, 1200);
      },
      dataType: "json"
    });
    return false;
  })
}


function registerAction(cookie_id, action, details){
  $.ajax({
    type: "POST",
    url: "http://139.59.24.127:8080/api/registerAction",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify({"cookie_id": cookie_id, "action":action, "details":details}),
    success: function(data){
      console.log(data);
      $("#path").find("tr:gt(0)").remove();
      populateTable(data)
      },
    dataType: "json"
  });
}

function listenClickAction(button_id){
  $(button_id).click(function(){
    console.log("clickAction", button_id);
    action = "click";
    details = $(button_id).text();
    cookie_id = Cookies.getJSON("coherence")['cookie_id']
    registerAction(cookie_id, action, details)
  });
}

function getAllPaths() {
  $.ajax({
    type: "POST",
    url: "http://139.59.24.127:8080/api/getAllPaths",
    contentType: "application/json; charset=utf-8",
    data: null,
    success: function(data){
      console.log(data);
      $("#path").find("tr:gt(0)").remove();
      populateTable(data)
      },
    dataType: "json"
  });
}


function populateTable(data){
  $(function() {
      $.each(data, function(i, item) {
          var $tr = $('#path').append(
            $('<tr>').append(
              $('<td>').text(item.id),
              $('<td>').text(item.timestamp),
              $('<td>').text(item.name),
              $('<td>').text(item.action),
              $('<td>').text(item.details)
          )); //.appendTo('#records_table');
          console.log($tr.wrap('<p>').html());
      });
  });
}
