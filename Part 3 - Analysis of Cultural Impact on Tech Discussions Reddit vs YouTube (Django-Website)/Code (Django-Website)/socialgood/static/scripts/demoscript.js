
    $(document).ready(function($) {
        $("#da").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader1").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader1").hide();
                    // Refresh the page
                    location.reload();

                    // Call the openModal function after a short delay (e.g., 1000 milliseconds or 1 second)
                    setTimeout(openModal, 1000); 

                    //$('#modalImage1').modal('show');
                },
                
                error: function(error) {
                    // Handle errors if needed
                    $(".loader1").hide();
                    console.error(error);
                }
            });
        });
    });


    $(document).ready(function($) {
        $("#db").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader2").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader2").hide();
                    // Refresh the page
                    location.reload(); 
                    //$('#modalImage2').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader2").hide();
                    console.error(error);
                }
            });
        });
    });

    
    $(document).ready(function($) {
        $("#dc").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader3").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader3").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage3').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader3").hide();
                    console.error(error);
                }
            });
        });
    });

    $(document).ready(function($) {
        $("#dd").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader4").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader4").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage4').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader4").hide();
                    console.error(error);
                }
            });
        });
    });

    $(document).ready(function($) {
        $("#de").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader5").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader5").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage5').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader5").hide();
                    console.error(error);
                }
            });
        });
    });

    $(document).ready(function($) {
        $("#df").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader6").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader6").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage6').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader6").hide();
                    console.error(error);
                }
            });
        });
    });

    $(document).ready(function($) {
        $("#dg").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader7").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader7").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage7').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader7").hide();
                    console.error(error);
                }
            });
        });
    });

    $(document).ready(function($) {
        $("#dh").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader8").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader8").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage8').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader8").hide();
                    console.error(error);
                }
            });
        });
    });

    $(document).ready(function($) {
        $("#di").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader9").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader9").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage9').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader9").hide();
                    console.error(error);
                }
            });
        });
    });


    $(document).ready(function($) {
        $("#dj").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader10").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader10").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage10').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader10").hide();
                    console.error(error);
                }
            });
        });
    });

    $(document).ready(function($) {
        $("#dk").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader11").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader11").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage11').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader11").hide();
                    console.error(error);
                }
            });
        });
    });


    $(document).ready(function($) {
        $("#fda").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader121").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader121").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage11').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader121").hide();
                    console.error(error);
                }
            });
        });
    });


    $(document).ready(function($) {
        $("#fdb").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader122").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader122").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage11').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader122").hide();
                    console.error(error);
                }
            });
        });
    });


    $(document).ready(function($) {
        $("#fdc").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader123").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader123").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage11').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader123").hide();
                    console.error(error);
                }
            });
        });
    });

    $(document).ready(function($) {
        $("#fdd").on("click", function() {
            // Make an AJAX request to your Django view
            $(".loader124").show();
            // Retrieve the URL from the data attribute
            var url = $(this).data("url");
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    // Handle the response if needed
                    console.log(response);

                    // Trigger the modal after the AJAX request is complete
                    $(".loader124").hide();
                    // Refresh the page
                    location.reload();
                    //$('#modalImage11').modal('show');
                },
                error: function(error) {
                    // Handle errors if needed
                    $(".loader124").hide();
                    console.error(error);
                }
            });
        });
    });