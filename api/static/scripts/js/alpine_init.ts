import Alpine from 'alpinejs';
import mask from '@alpinejs/mask';
import persist from '@alpinejs/persist';
import collapse from '@alpinejs/collapse';
import focus from '@alpinejs/focus';
// import axios from 'axios';
import comics from './comics';
import comic from './comic';
import chapter from './chapter';
import slider from './slider';
// interface ComicsResponse {
//     next: string;
//     previous: string;
//     count: number;
//     items: string[];
// }
// interface TopComicsResponse {
//     slides: any;
//     currentSlideIndex: number;
// }

// interface ComicResponse {
//     comicchapters: any[];
//     comicitems: any[];
//     showPoster: boolean;
//     comicitem: any;
// }
// interface ChapterResponse {
//     chapteritem: any;
//     chapteritems: any[];
// }

window.Alpine = Alpine;

Alpine.plugin(mask);
Alpine.plugin(persist);
Alpine.plugin(focus);
Alpine.plugin(collapse);
Alpine.data('comics', comics);
Alpine.data('slider', slider);
Alpine.data('comic', comic);
Alpine.data('chapter', chapter);
// Alpine.store('appStore', {
//     items: Alpine.$persist([]).as('items'),

//     next: Alpine.$persist('').as('next'),
//     previous: Alpine.$persist('').as('previous'),
//     count: Alpine.$persist(0).as('count'),
//     showPoster: false,
//     comicitem: Alpine.$persist({}).as('comicitem'),
//     chapteritem: Alpine.$persist({}).as('chapteritem'),
//     search: '',
//     slides: [],
//     currentSlideIndex: 1,
//     tprevious(this: TopComicsResponse) {
//         if (this.currentSlideIndex > 1) {
//             this.currentSlideIndex = this.currentSlideIndex - 1;
//         } else {
//             this.currentSlideIndex = this.slides.length;
//         }
//     },
//     tnext(this: TopComicsResponse) {
//         if (this.currentSlideIndex < this.slides.length) {
//             this.currentSlideIndex = this.currentSlideIndex + 1;
//         } else {
//             this.currentSlideIndex = 1;
//         }
//     },
//     async toggleComics(this: ComicsResponse, url: string) {
//         const curl = url;
//         const options = {
//             method: 'GET',
//             url: curl,
//             // params: { keyword: 'all', page: '1' },
//             headers: {},
//         };
//         await axios
//             .request(options)
//             .then(({ data }: { data: ComicsResponse }) => {
//                 this.items = data?.items;
//                 this.next = data?.next;
//                 this.previous = data?.previous;
//                 this.count = data?.count;
//             })
//             .catch(function (error: any) {
//                 console.error(error);
//             });
//     },
//     async toggleTopComics(this: TopComicsResponse, url: string) {
//         const curl = url;
//         const options = {
//             method: 'GET',
//             url: curl,
//             // params: { keyword: 'all', page: '1' },
//             headers: {},
//         };
//         await axios
//             .request(options)
//             .then(({ data }: { data: TopComicsResponse }) => {
//                 this.slides = data;
//             })
//             .catch(function (error: any) {
//                 console.error(error);
//             });
//     },
//     async toggleComic(this: ComicResponse, id: number) {
//         const cid = id;
//         const options = {
//             method: 'GET',
//             url: `/api/comics/${cid}/`,
//             // params: { keyword: 'all', page: '1' },
//             headers: {},
//         };
//         await axios
//             .request(options)
//             .then(({ data }: { data: ComicResponse }) => {
//                 this.comicitem = data;
//                 this.comicitem.firstchapter = data?.comicchapters[0];
//                 this.comicitem.lastchapter = data?.comicchapters[data?.comicchapters.length - 1];
//                 if (data?.comicitems.length > 1) {
//                     this.showPoster = true;
//                     this.comicitem.bigcover = data?.comicitems[1];
//                 }
//             })
//             .catch(function (error: any) {
//                 console.error(error);
//             });
//     },
//     async toggleChapter(this: ChapterResponse, id: number) {
//         const cid = id;
//         const options = {
//             method: 'GET',
//             url: `/api/chapters/${cid}/`,
//             // params: { keyword: 'all', page: '1' },
//             headers: {},
//         };
//         await axios
//             .request(options)
//             .then(({ data }: { data: ChapterResponse }) => {
//                 this.chapteritem = data;
//                 this.chapteritem.chapteritems = data?.chapteritems;
//             })
//             .catch(function (error: any) {
//                 console.error(error);
//             });
//     },

//     name: 'RhixeScans',
// });
Alpine.start();
