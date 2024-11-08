import axios from 'axios';
export default () => ({
  slides: [],
  currentSlideIndex: 1,
  init() {
    this.load('/api/comics/top/');
  },
  load(url) {
    const link = url;
    const options = {
      method: 'GET',
      url: link,
      headers: {},
    };
    axios
      .request(options)
      .then((data) => {
        this.slides = data.data;
      })
      .catch(function (error) {
        console.error(error);
      });
  },
  previous() {
    if (this.currentSlideIndex > 1) {
      this.currentSlideIndex = this.currentSlideIndex - 1;
    } else {
      this.currentSlideIndex = this.slides.length;
    }
  },
  next() {
    if (this.currentSlideIndex < this.slides.length) {
      this.currentSlideIndex = this.currentSlideIndex + 1;
    } else {
      this.currentSlideIndex = 1;
    }
  },
});
