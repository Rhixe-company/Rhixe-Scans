import axios from 'axios';
export default () => ({
  data: [],
  init() {
    this.load('/api/comics/');
  },
  load(url) {
    const link = url;
    const options = {
      method: 'GET',
      url: link,
      headers: { 'Content-type': 'application/json' },
    };
    axios
      .request(options)
      .then((data) => {
        this.data = data.data;
      })
      .catch(function (error) {
        console.error(error);
      });
  },
});
