$(document).ready(function()
        {
            $('#calendar').fullCalendar(
            {
                //Event's info - JSON
                events:"events/",

                //Calendar Config
                firstDay:1, //start with Monday
                lang:"fr",  //French
                header:{
                            left:   'title',
                            center: '',
                            right:  'today prev,next', //prev and next arrows position in header
                        },
                height:"auto", //show all weeks with no scrollbar
                fixedWeekCount:false, //adjust number of weeks 4, 5 or 6 automatically
                theme:false,   //can be overwridden with JQuery themes to change bottons format

                //Calendar Function
                 eventClick:function(event, jsEvent, view)
                 {
                    //Title
                    document.getElementById('event_title').innerHTML = event.title;
                    document.getElementById('project_logo').src = event.project_logo;
                    document.getElementById('project_logo').innerHTML = event.title;
                    //Description & details
                    $('#event_description').html(event.description);
                    $('#project_name').html(event.project_name);
                    //$('#event_place').html(event.place);
                    $('#contact_name').html(event.contact_name);
                    $('#contact_phone').html(event.contact_phone);
                    $('#contact_email').html(event.contact_email);
                    //$('#inscription').html(event.inscription);
                    document.getElementById('project_site').href = event.project_site;

                    $('#project_site').html(event.project_site);
                    $('#fullcalmodal').modal();

                    // debug info :
//                    alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
//                    alert('View: ' + view.name);
                    // change the border color just for fun
//                    $(this).css('border-color', 'red');
                 }
            })
        })
