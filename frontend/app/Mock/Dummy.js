import { images } from '../../constants';

export const Playlists = [{
    id: '001',
    name: 'Rap',
    songs: 15,
    thumbnail: require('../../assets/images/unknown_track.png'),
  },
  {
    id: '002',
    name: 'Relax',
    songs: 26,
    thumbnail: require('../../assets/images/unknown_track.png'),
  },
  {
    id: '003',
    name: 'Театр',
    songs: 6,
    thumbnail: require('../../assets/images/unknown_track.png'),
  },
];

export const Favorite = [{
    id: '001',
    url: '',
    title: 'Кров і вино',
    album: 'Твій Віль del.1',
    artist: 'Schmalgauzen',
    thumbnail: require('../../assets/playlists/schmalgauzen.jpg'),
  },
  {
    id: '002',
    url: '',
    title: 'Шукали вчора',
    album: 'Недовготривалі відносини',
    artist: 'Otoy',
    thumbnail: require('../../assets/playlists/otoy.jpg'),
  },
  {
    id: '003',
    url: '',
    title: 'Місто Весни',
    album: 'Сингл',
    artist: 'Океан Ельзи ft. Один в каное',
    thumbnail: require('../../assets/playlists/misto-vesny.jpg'),
  },
  {
    id: '004',
    url: '',
    title: 'Поки ніхто не бачить',
    album: 'Буденна пересічна драма',
    artist: 'Макс Пташник',
    thumbnail: require('../../assets/playlists/poky-nihto.jpg'),
  },
];

export const Songs = [{
  id: '001',
  url: require('../../assets/songs/krovivyno.mp3'),
  title: 'Кров і вино',
  album: 'Твій Віль del.1',
  artist: 'Schmalgauzen',
  thumbnail: require('../../assets/playlists/schmalgauzen.jpg'),
  playlistname: 'Театр',
  genrename: 'Поп',
},
{
  id: '002',
  url: require('../../assets/songs/shukalyvchora.mp3'),
  title: 'Шукали вчора',
  album: 'Недовготривалі відносини',
  artist: 'Otoy',
  thumbnail: require('../../assets/playlists/otoy.jpg'),
  playlistname: 'Rap',
  genrename: 'Хіп-хоп',
},
{
  id: '003',
  url: require('../../assets/songs/mistovesny.mp3'),
  title: 'Місто Весни',
  album: 'Сингл',
  artist: 'Океан Ельзи ft. Один в каное',
  thumbnail: require('../../assets/playlists/misto-vesny.jpg'),
  playlistname: 'Театр',
  genrename: 'Поп',
},
{
  id: '004',
  url: require('../../assets/songs/pokynihto.mp3'),
  title: 'Поки ніхто не бачить',
  album: 'Буденна пересічна драма',
  artist: 'Макс Пташник',
  thumbnail: require('../../assets/playlists/poky-nihto.jpg'),
  playlistname: 'Relax',
  genrename: 'Бандура',
},
{
  id: '005',
  url: require('../../assets/songs/pokynihto.mp3'),
  title: 'Тетяна',
  album: 'Твій Віль',
  artist: 'Schmalgauzen',
  thumbnail: require('../../assets/playlists/schmalgauzen.jpg'),
  playlistname: 'Театр',
  genrename: 'Бандура',
},
{
  id: '006',
  url: '',
  title: 'Jessica',
  album: 'Твій Віль',
  artist: 'Schmalgauzen',
  thumbnail: require('../../assets/playlists/schmalgauzen.jpg'),
  playlistname: 'Театр',
  genrename: 'Бандура',
},
{
  id: '007',
  url: '',
  title: 'Cherkaschyna',
  album: '',
  artist: 'LATEXFAUNA',
  thumbnail: require('../../assets/playlists/latexfauna-cherkaschyna.jpg'),
  genrename: 'Вірал Поп',
},
{
  id: '008',
  url: '',
  title: 'Sequoia',
  album: '',
  artist: 'LATEXFAUNA',
  thumbnail: require('../../assets/playlists/latexfauna-cherkaschyna.jpg'),
  playlistname: 'Театр',
  genrename: 'Вірал Поп',
},
{
  id: '009',
  url: '',
  title: 'етнокод',
  album: '',
  artist: 'Otoy',
  thumbnail: require('../../assets/playlists/otoy.jpg'),
  playlistname: 'Rap',
  genrename: 'Вірал Поп',
},
];

export const Artists = [{
    id: '001',
    name: 'Schmalgauzen',
    thumbnail: require('../../assets/playlists/schmalgauzen.jpg'),
  },
  {
    id: '002',
    name: 'Otoy',
    thumbnail: require('../../assets/playlists/otoy.jpg'),
  },
  {
    id: '003',
    name: 'The Hardkiss',
    thumbnail: require('../../assets/playlists/hardkiss-zhyva.webp'),
  },
  {
    id: '004',
    name: 'LATEXFAUNA',
    thumbnail: require('../../assets/playlists/latexfauna-cherkaschyna.jpg'),
  },
  {
    id: '005',
    name: 'Carpetman',
    thumbnail: require('../../assets/playlists/my-honey.jpg'),
  },
];

export const Genre = [{
    id: '001',
    name: 'Поп',
    thumbnail: (images.category1)
  },
  {
    id: '002',
    name: 'Вірал Поп',
    thumbnail: (images.category2)
  },
  {
    id: '003',
    name: 'Рок',
    thumbnail: (images.category3)
  },
  {
    id: '004',
    name: 'Інді',
    thumbnail: (images.category4)
  },
  {
    id: '005',
    name: 'Бандура',
    thumbnail: (images.category5)
  },
  {
    id: '006',
    name: 'Хіп-хоп',
    thumbnail: (images.category6)
  },
  {
    id: '007',
    name: 'Панк',
    thumbnail: (images.category7)
  },
  {
    id: '008',
    name: 'Класичний рок',
    thumbnail: (images.category8)
  },
];
  
  const dummyData = { Playlists, Favorite, Songs, Artists, Genre };
  
  export default dummyData;
