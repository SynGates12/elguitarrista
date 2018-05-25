var sliders = {
  1: {slider : '#slider_1', nav: '#slider_nav_1'},
  2: {slider : '#slider_2', nav: '#slider_nav_2'},
  3: {slider : '#slider_3', nav: '#slider_nav_3'}
};

$.each(sliders, function() {

  $(this.slider).slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: this.nav
  });
  $(this.nav).slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    asNavFor: this.slider,
    dots: true,
    arrows: true,
    centerMode: false,
    focusOnSelect: true
  });

});