// Wrap every letter in a span
$('.titlefooter').each(function(){
  $(this).html($(this).text().replace(/([^\x00-\x80]|\w)/g, "<span class='letter2'>$&</span>"));
});

anime.timeline({loop: true})
  .add({
    targets: '.titlefooter .letter2',
    opacity: [0,1],
    easing: "easeInOutQuad",
    duration: 2250,
    delay: function(el, i) {
      return 150 * (i+1)
    }
  }).add({
    targets: '.titlefooter',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 1000
  });
