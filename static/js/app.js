(function() {

	$(document).ready(function() {

		var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
		var weekdayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

		// Fade in once weather loads
		$('.container').hide();

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
					$('.container').fadeIn(1500);
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

		// QUOTES
		function getQuote() {
			// TODO: Scrape this in python, add to DB and pull from Flask - http://www.forbes.com/sites/kevinkruse/2013/05/28/inspirational-quotes/
			var quotes = [
				{
					content: "Life is about making an impact, not making an income",
					author: "Kevin Kruse"
				},{
					content: " Whatever the mind of man can conceive and believe, it can achieve",
					author: " Napoleon Hill"
				},{
					content: "I’ve missed more than 9000 shots in my career. I’ve lost almost 300 games. 26 times I’ve been trusted to take the game winning shot and missed. I’ve failed over and over and over again in my life. And that is why I succeed.",
					author: "Michael Jordan"
				},{
					content: "We become what we think about",
					author: "Earl Nightingale"
				},{
					content: "Life is 10% what happens to me and 90% of how I react to it.",
					author: "Charles Swindoll"
				},{
					content: "The mind is everything. What you think you become",
					author: "Buddha"
				},{
					content: "Eighty percent of success is showing up",
					author: "Woody Allen"
				},{
					content: "I am not a product of my circumstances. I am a product of my decisions",
					author: "Stephen Covey"
				},{
					content: "I’ve learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.",
					author: "Maya Angelou"
				},{
					content: "Whether you think you can or you think you can’t, you’re right",
					author: "Henry Ford"
				},{
					content: "However difficult life may seem, there is always something you can do and succeed at",
					author: "Stephen Hawking"
				},{
					content: "What are thooooooose?",
					author: "Ryan Shave"
				}
			];

			var randomQuote = quotes[Math.floor(Math.random() * quotes.length)];

			$('.quote-content').html(randomQuote.content);
			$('.quote-author').html(randomQuote.author);
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
				$('.calendar').hide();

				table = $('<table/>').addClass('xsmall').addClass('calendar-table');
				opacity = 1;


				for (var i in cal) {
					var c = cal[i];
					var row = $('<tr/>').attr('id', 'event'+i).css('opacity',opacity).addClass('event');
					row.append($('<td/>').html(c.summary).addClass('description'));
					row.append($('<td/>').html(c.date).addClass('days dimmed'));
					table.append(row);
					//opacity -= 1 / cal.length;
				};

				$('.calendar').show();
				$('.calendar').append(table);
				console.log(table);
			});
		}		

		startTime();
		getWeather();
		getQuote();
		getNews();
		getCal();
		//calendar.init();
	});

})();
