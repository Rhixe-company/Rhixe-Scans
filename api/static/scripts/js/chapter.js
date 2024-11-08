import axios from 'axios';
export default () => ({
  data: [],
  chapteritems: [],
  chapters: [],
  expanded: false,
  expanded1: false,
  currentSlideIndex: 1,
  load(id) {
    const cid = id;
    const options = {
      method: 'GET',
      url: `/api/chapters/${cid}/`,
      headers: { 'Content-type': 'application/json' },
    };
    axios
      .request(options)
      .then((data) => {
        this.data = data?.data;
        this.chapteritems = data?.data.chapteritems;
        this.chapters = data.data?.chapters;
      })
      .catch(function (error) {
        console.error(error);
      });
  },
  previous() {
    if (this.currentSlideIndex > 1) {
      this.currentSlideIndex = this.currentSlideIndex - 1;
    } else {
      this.currentSlideIndex = this.chapters.length;
    }
  },
  next() {
    if (this.currentSlideIndex < this.chapters.length) {
      this.currentSlideIndex = this.currentSlideIndex + 1;
    } else {
      this.currentSlideIndex = 1;
    }
  },
});
