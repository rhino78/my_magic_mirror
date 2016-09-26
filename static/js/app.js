(function() {

	$(document).ready(function() {

		var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
		var weekdayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

		// Fade in once weather loads
		$('.container').show(1500);

		// TIME
		function checkTime(i) {
			return (i < 10) ? "0" + i : i;
    }

    jQuery.fn.updateWithText = function(text, speed)
{
	var dummy = $('<div/>').html(text);

	if ($(this).html() != dummy.html())
	{
		$(this).fadeOut(speed/2, function() {
			$(this).html(text);
			$(this).fadeIn(speed/2, function() {
				//done
			});
		});
	}
}

    function startTime() {
    	var today, h, h_mod, m, s, am_pm;

      today = new Date();
      h = checkTime(today.getHours());
      m = checkTime(today.getMinutes());
      s = checkTime(today.getSeconds());

      am_pm = h < 12 ? 'am' : 'pm';
      h_mod = h < 12 ? h : h - 12;

      if (h == 0) {
      	h_mod = 12;      	
      } else if (h == 12) {
      	h_mod = 12;
      } else if (h < 12) {
      	h_mod = h;
      } else {
      	h_mom = h - 12;
      }
      
      //see if we can get the day in here also

      $(".full-date").html(
		weekdayNames[today.getDay()]
      	+",  " +
      	monthNames[today.getMonth()] 
      	+ " " + 
      	today.getDate());
      $(".timer-hour").html(h_mod);
      $(".timer-min").html(m);
      $(".timer-suffix").html(am_pm);
      t = setTimeout(function () {
				startTime()
			}, 500);
    }

    // WEATHER
    function getWeather() {
			$.ajax({
				type: 'GET',
				dataType: 'jsonp',
				url: "https://api.forecast.io/forecast/" + config.weather_api_key + "/" + config.location.latitude + "," + config.location.longitude,
				success: function(data) {
					formatWeather(data);
					$('.container').show(1500);
				}
			});
		}

		function formatWeather(weather) {
			var days = ['Sun', 'Mon', 'Tu', 'Wed', 'Th', 'Fri', 'Sat'];			
		  var dayOfWeek = new Date().getDay();
		  var arrangedDays = (days.splice(dayOfWeek)).concat(days);

		  // current weather
			$('.current-temp').html(Math.round(weather.currently.temperature));
			$('.current-weather-icon').addClass(weatherIcons[weather.currently.icon]);
			//$('.prob-rain').html(Math.round(weather.daily.data[0].precipProbability * 100));

			console.log(weather);
			// hourly change weather
			for (var j = 1; j <= 12; j+=3) {
				var time = new Date(weather.hourly.data[j].time * 1000);
				var hour = time.getHours();

				if (hour > 12) {
					hour = hour - 12 + 'PM';
				} else if (hour === 0) {
					hour = 12 + 'AM';
				} else {
					hour += 'AM';
				}

				$('.hourly-change-container').append("<div class='hourly-change'></div>");
				$('.hourly-change').last().append("<span class='hourly-change-label'>" + hour + " </span>");
				$('.hourly-change').last().append("<span class='" + weatherIcons[weather.hourly.data[j].icon] + "'</span>");
				$('.hourly-change').last().append("<span> " + Math.round(weather.hourly.data[j].temperature) + "º </span>");
			}
			
			// daily weather
			for (var i = 0; i < 7; i++) {
				$('.weekly-forecast-container').append("<div class='weekly-forecast-day'></div>");
				$('.weekly-forecast-day').last().append("<span class='day-label'>" + arrangedDays[i] + " </span>");
				$('.weekly-forecast-day').last().append("<span class='" + weatherIcons[weather.daily.data[i].icon] +"'></span>");
				$('.weekly-forecast-day').last().append("<span> " + Math.round(weather.daily.data[i].temperatureMax) + "º</span> / <span>" + Math.round(weather.daily.data[i].temperatureMin) + "º </span>");
			}
		}
		function getCompliment(){
			$.get("/get_compliment", function (data){
				var complimemt = data.compliment;
				$('.compliment').html(complimemt).show(1500);
			});
		}

		// NEWS TICKER
		function getNews() {
			$.get("/get_news_headlines", function (data) {
				var headlines = data.headlines.slice(0, 10); // just get the first 10 because they get crappy after that
				$('.marquee').hide();
				
				headlines.forEach(function(headline) {
					$('.marquee').append("<li>" + headline.description + "</li>");
					$('.marquee').append("<li class='wi wi-hurricane'></li>");
				});

				setTimeout(function() {
					$('.marquee').show();

					// https://jsfiddle.net/ymdahi/sj2Lcq6x/
					$('.marquee').marquee({
		        duration: 8000,
		        duplicate: false
			    });
				}, 1000);
				
			});
		}

		//Ical
		function getCal() {
			$.get("/get_calendar", function (data) {
				var cal = data.calendar.slice(0, 20); //let's just get the first ten for now
				var _is_new = true;
				$('.calendar').show(1500);

				table = $('<table/>').addClass('xsmall').addClass('calendar-table');
				opacity = 1;


				for (var i in cal) {
					var c = cal[i];
					var row = $('<tr/>').attr('id', 'event'+i).css('opacity',opacity).addClass('event');
					row.append($('<td/>').html(c.summary.substring(0,50)).addClass('description'));
					row.append($('<td/>').html(c.date).addClass('days dimmed'));
					table.append(row);
					opacity -= 1 / cal.length;
				};


				$('.calendar').append(table);
			});
		}

		function getEPL() {
			$.get("/get_epl", function (data) {
				
				var the_table = data.epl;
				var _is_new = true;
				$('.epl_table').show(1500);

				table = $('<table/>').addClass('xsmall').addClass('epl-table');
				opacity = 1;

					var row = $('<tr/>').attr('id', 'pos0').css('opacity',opacity).addClass('table');
					row.append($('<td/>').html("Movement").addClass('table'));
					row.append($('<td/>').html("Pos").addClass('table'));
					row.append($('<td/>').html("").addClass('table'));
					row.append($('<td/>').html("Name").addClass('table'));
					row.append($('<td/>').html("Played").addClass('table'));
					row.append($('<td/>').html("Won").addClass('table'));
					row.append($('<td/>').html("Draw").addClass('table'));
					row.append($('<td/>').html("Lost").addClass('table'));
					row.append($('<td/>').html("For").addClass('table'));
					row.append($('<td/>').html("Against").addClass('table'));
					row.append($('<td/>').html("Goal Diff").addClass('table'));
					row.append($('<td/>').html("Points").addClass('table'));
					row.append($('<td/>').html("Form").addClass('form'));
					table.append(row);

				for (var i = 0; i < 19; i++) {
					var e = the_table[i];
					var row = $('<tr/>').attr('id', 'pos'+e.position).css('opacity',opacity).addClass('table');
					console.log(e.movement);
					if (e.movement == "No movement") {
						row.append($('<td/>').html("-").addClass('table'));
					}else if (e.movement == "Moving up") {
						row.append($('<td/>').html("^").addClass('table'));

					}else{
						row.append($('<td/>').html("v").addClass('table'));

					}
					
					row.append($('<td/>').html(e.position).addClass('table'));
					row.append($('<td/>').html("icon").addClass('table').innerHTML = "<img src='/static/images/"+ e.name +".png' style='width:30px; height:30px;'/>");
					row.append($('<td/>').html(e.name).addClass('table'));
					row.append($('<td/>').html(e.p).addClass('table'));
					row.append($('<td/>').html(e.w).addClass('table'));
					row.append($('<td/>').html(e.d).addClass('table'));
					row.append($('<td/>').html(e.l).addClass('table'));
					row.append($('<td/>').html(e.f).addClass('table'));
					row.append($('<td/>').html(e.a).addClass('table'));
					row.append($('<td/>').html(e.gd).addClass('table'));
					row.append($('<td/>').html(e.pt).addClass('table'));
					

					var form ="";
					for (var g in e.last_5){
						game = e.last_5[g];
						form = form + game.substring(0,1) + "-";
					};
					//ex W-W-W-W-W

					row.append($('<td/>').html(form.substring(0, form.length -1)).addClass('form'));


					table.append(row);						
					};


				$('.epl_table').append(table);
			});
		}		

		getEPL();
		startTime();
		getWeather();
		getCompliment();
		getNews();
		getCal();
		
	});

})();
