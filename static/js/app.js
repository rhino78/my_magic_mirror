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
				h_mod = h - 12;
			}

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
			$.get("/get_weather", function (data){
				formatWeather(data);
			$('.container').show(1500);
			});
		}

		function translateHour(hour){
			results ="";
			switch(hour){
				case "0":
					results = '12AM';
					break;
				case "300":
					results = '3AM'
					break;
				case "600":
					results = '6AM'
					break;
				case "900":
					results = '9AM'
					break;
				case "1200":
					results = '12PM'
					break;
				case "1500":
					results = '3PM'
					break;
				case "1800":
					results = '6PM'
					break;
				case "2100":
					results = '9PM'
					break;
			}
			return results;
		}

		function formatWeather(weather) {
			var days = ['Sun', 'Mon', 'Tu', 'Wed', 'Th', 'Fri', 'Sat'];
		  var dayOfWeek = new Date().getDay();
		  var arrangedDays = (days.splice(dayOfWeek)).concat(days);

		  // current weather
			$('.current-temp').html(JSON.parse(weather['weather']['current_condition'][0]['FeelsLikeF']));
			$('.current-weather-icon').addClass(weatherIDIcons[JSON.parse(weather['weather']['current_condition'][0]['weatherCode'])]);

			// hourly change weather
			for (var j = 0; j <= 7; j+=1) {
				var hour = translateHour(weather['weather']['weather'][0]['hourly'][j]['time']);

				$('.hourly-change-container').append("<div class='hourly-change'></div>");
				$('.hourly-change').last().append("<span class='hourly-change-label'>" + hour + " </span>");
				$('.hourly-change').last().append("<span class='" + weatherIDIcons[JSON.parse(weather['weather']['weather'][0]['hourly'][j]['weatherCode'])] + "'</span>" );
				$('.hourly-change').last().append("<span> " + JSON.parse(weather['weather']['weather'][0]['hourly'][j]['FeelsLikeF']) + "º </span>");
			}

			// daily weather
			for (var i = 0; i < 3; i++) {
				$('.weekly-forecast-container').append("<div class='weekly-forecast-day'></div>");
				$('.weekly-forecast-day').last().append("<span class='day-label'>" + arrangedDays[i] + " </span>");
				$('.weekly-forecast-day').last().append("<span class='" + weatherIDIcons[JSON.parse(weather['weather']['weather'][i]['hourly'][0]['weatherCode'])] +"'></span>");
				$('.weekly-forecast-day').last().append("<span> " + JSON.parse(weather['weather']['weather'][i]['maxtempF']) + "º</span> / <span>" + JSON.parse(weather['weather']['weather'][i]['mintempF']) + "º </span>");
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

		startTime();
		getWeather();
		getCompliment();
		getNews();
		getCal();

	});

})();
