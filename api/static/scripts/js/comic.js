import axios from 'axios';
export default () => ({
  data: [],
  showPoster: false,
  poster: [],
  gal: [],
  fchapter: [],
  lchapter: [],
  load(id) {
    const cid = id;
    const options = {
      method: 'GET',
      url: `/api/comics/${cid}/`,
      headers: { 'Content-type': 'application/json' },
    };
    axios
      .request(options)
      .then((data) => {
        this.data = data?.data;
        this.gal = data?.data.comicitems[0];
        this.fchapter =
          data.data?.comicchapters[data.data?.comicchapters?.length - 1];
        this.lchapter = data.data?.comicchapters[0];
        if (data?.data.comicitems.length == 2) {
          this.showPoster = true;
          this.poster = data?.data.comicitems[1];
        }
      })
      .catch(function (error) {
        console.error(error);
      });
  },
});
