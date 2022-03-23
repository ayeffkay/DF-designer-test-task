$.ajax({
    type: "POST",
    url: "/get_window_size",
    contentType: "application/json",
    data: JSON.stringify({"width": $(document).height(), "height": $(document).width()}),
    dataType: "json",
    success: function(response) {
        console.log(response);
    },
    error: function(err) {
        console.log(err);
    }
});
