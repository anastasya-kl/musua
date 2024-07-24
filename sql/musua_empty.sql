-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июл 24 2024 г., 15:44
-- Версия сервера: 10.4.19-MariaDB
-- Версия PHP: 7.4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `musua_empty`
--

-- --------------------------------------------------------

--
-- Структура таблицы `albums`
--

CREATE TABLE `albums` (
  `id` varchar(22) NOT NULL,
  `name` varchar(100) NOT NULL,
  `release_date` date NOT NULL,
  `album_total_tracks` tinyint(4) NOT NULL,
  `background` text NOT NULL,
  `type` varchar(6) NOT NULL,
  `popularity` tinyint(3) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `artists`
--

CREATE TABLE `artists` (
  `id` varchar(22) NOT NULL,
  `name` varchar(100) NOT NULL,
  `popularity` tinyint(3) UNSIGNED NOT NULL,
  `photo` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `artist_albums`
--

CREATE TABLE `artist_albums` (
  `id_artist` varchar(22) NOT NULL,
  `id_album` varchar(22) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `artist_genres`
--

CREATE TABLE `artist_genres` (
  `id_artist` varchar(22) NOT NULL,
  `id_genre` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `artist_songs`
--

CREATE TABLE `artist_songs` (
  `id_artist` varchar(22) NOT NULL,
  `id_song` varchar(22) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `categories`
--

CREATE TABLE `categories` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(100) NOT NULL,
  `genre_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `genres`
--

CREATE TABLE `genres` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(100) NOT NULL,
  `simple_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `playlists`
--

CREATE TABLE `playlists` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `cover` tinyint(1) NOT NULL DEFAULT 0,
  `id_user` varchar(20) DEFAULT NULL,
  `creation_date` datetime NOT NULL,
  `for_user_id` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `playlist_songs`
--

CREATE TABLE `playlist_songs` (
  `id_playlist` bigint(20) UNSIGNED NOT NULL,
  `id_song` varchar(22) NOT NULL,
  `insert_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `playlist_tags`
--

CREATE TABLE `playlist_tags` (
  `id_playlist` bigint(20) UNSIGNED NOT NULL,
  `tag` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `prefixes`
--

CREATE TABLE `prefixes` (
  `album_cover` varchar(25) NOT NULL DEFAULT 'https://i.scdn.co/image/',
  `track_mp3` varchar(14) NOT NULL DEFAULT 'spotify:track:',
  `preview_url` varchar(30) NOT NULL DEFAULT 'https://p.scdn.co/mp3-preview/'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `prefixes`
--

INSERT INTO `prefixes` (`album_cover`, `track_mp3`, `preview_url`) VALUES
('https://i.scdn.co/image/', 'spotify:track:', 'https://p.scdn.co/mp3-preview/');

-- --------------------------------------------------------

--
-- Структура таблицы `songs`
--

CREATE TABLE `songs` (
  `id` varchar(22) NOT NULL,
  `name` varchar(100) NOT NULL,
  `duration_ms` int(10) UNSIGNED NOT NULL,
  `track_number` tinyint(4) NOT NULL,
  `id_album` varchar(22) NOT NULL,
  `preview_url_id` varchar(40) DEFAULT NULL,
  `popularity` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `song_genres`
--

CREATE TABLE `song_genres` (
  `id_genre` bigint(20) UNSIGNED NOT NULL,
  `id_song` varchar(22) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` varchar(20) NOT NULL,
  `nickname` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `user_favourite_albums`
--

CREATE TABLE `user_favourite_albums` (
  `id_user` varchar(20) NOT NULL,
  `id_album` varchar(22) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `user_favourite_playlists`
--

CREATE TABLE `user_favourite_playlists` (
  `id_user` varchar(20) NOT NULL,
  `id_playlist` bigint(20) UNSIGNED NOT NULL,
  `addition_date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `user_favourite_songs`
--

CREATE TABLE `user_favourite_songs` (
  `id_user` varchar(20) NOT NULL,
  `id_song` varchar(22) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `albums`
--
ALTER TABLE `albums`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `id_2` (`id`);

--
-- Индексы таблицы `artists`
--
ALTER TABLE `artists`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Индексы таблицы `artist_albums`
--
ALTER TABLE `artist_albums`
  ADD KEY `id_artist` (`id_artist`),
  ADD KEY `id_song` (`id_album`);

--
-- Индексы таблицы `artist_genres`
--
ALTER TABLE `artist_genres`
  ADD KEY `id_artist` (`id_artist`),
  ADD KEY `id_genre` (`id_genre`);

--
-- Индексы таблицы `artist_songs`
--
ALTER TABLE `artist_songs`
  ADD KEY `id_artist` (`id_artist`),
  ADD KEY `id_song` (`id_song`);

--
-- Индексы таблицы `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `genre_name` (`genre_name`);

--
-- Индексы таблицы `genres`
--
ALTER TABLE `genres`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `playlists`
--
ALTER TABLE `playlists`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `for_user_id` (`for_user_id`);

--
-- Индексы таблицы `playlist_songs`
--
ALTER TABLE `playlist_songs`
  ADD KEY `id_playlist` (`id_playlist`),
  ADD KEY `id_song` (`id_song`);

--
-- Индексы таблицы `playlist_tags`
--
ALTER TABLE `playlist_tags`
  ADD KEY `id_playlist` (`id_playlist`);

--
-- Индексы таблицы `prefixes`
--
ALTER TABLE `prefixes`
  ADD UNIQUE KEY `album_cover` (`album_cover`);

--
-- Индексы таблицы `songs`
--
ALTER TABLE `songs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `id_album` (`id_album`);

--
-- Индексы таблицы `song_genres`
--
ALTER TABLE `song_genres`
  ADD KEY `id_genre` (`id_genre`),
  ADD KEY `id_song` (`id_song`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `id_2` (`id`);

--
-- Индексы таблицы `user_favourite_albums`
--
ALTER TABLE `user_favourite_albums`
  ADD KEY `id_album` (`id_album`),
  ADD KEY `id_user` (`id_user`);

--
-- Индексы таблицы `user_favourite_playlists`
--
ALTER TABLE `user_favourite_playlists`
  ADD KEY `id_playlist` (`id_playlist`),
  ADD KEY `id_user` (`id_user`);

--
-- Индексы таблицы `user_favourite_songs`
--
ALTER TABLE `user_favourite_songs`
  ADD KEY `id_song` (`id_song`),
  ADD KEY `id_user` (`id_user`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `categories`
--
ALTER TABLE `categories`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `genres`
--
ALTER TABLE `genres`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `playlists`
--
ALTER TABLE `playlists`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `artist_albums`
--
ALTER TABLE `artist_albums`
  ADD CONSTRAINT `artist_albums_ibfk_1` FOREIGN KEY (`id_album`) REFERENCES `albums` (`id`),
  ADD CONSTRAINT `artist_albums_ibfk_2` FOREIGN KEY (`id_artist`) REFERENCES `artists` (`id`);

--
-- Ограничения внешнего ключа таблицы `artist_songs`
--
ALTER TABLE `artist_songs`
  ADD CONSTRAINT `artist_songs_ibfk_1` FOREIGN KEY (`id_artist`) REFERENCES `artists` (`id`),
  ADD CONSTRAINT `artist_songs_ibfk_2` FOREIGN KEY (`id_song`) REFERENCES `songs` (`id`);

--
-- Ограничения внешнего ключа таблицы `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`genre_name`) REFERENCES `genres` (`name`);

--
-- Ограничения внешнего ключа таблицы `playlists`
--
ALTER TABLE `playlists`
  ADD CONSTRAINT `playlists_ibfk_1` FOREIGN KEY (`for_user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `playlists_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `playlist_songs`
--
ALTER TABLE `playlist_songs`
  ADD CONSTRAINT `playlist_songs_ibfk_1` FOREIGN KEY (`id_playlist`) REFERENCES `playlists` (`id`),
  ADD CONSTRAINT `playlist_songs_ibfk_2` FOREIGN KEY (`id_song`) REFERENCES `songs` (`id`);

--
-- Ограничения внешнего ключа таблицы `playlist_tags`
--
ALTER TABLE `playlist_tags`
  ADD CONSTRAINT `playlist_tags_ibfk_1` FOREIGN KEY (`id_playlist`) REFERENCES `playlists` (`id`);

--
-- Ограничения внешнего ключа таблицы `songs`
--
ALTER TABLE `songs`
  ADD CONSTRAINT `songs_ibfk_1` FOREIGN KEY (`id_album`) REFERENCES `albums` (`id`);

--
-- Ограничения внешнего ключа таблицы `user_favourite_albums`
--
ALTER TABLE `user_favourite_albums`
  ADD CONSTRAINT `user_favourite_albums_ibfk_1` FOREIGN KEY (`id_album`) REFERENCES `albums` (`id`),
  ADD CONSTRAINT `user_favourite_albums_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `user_favourite_playlists`
--
ALTER TABLE `user_favourite_playlists`
  ADD CONSTRAINT `user_favourite_playlists_ibfk_2` FOREIGN KEY (`id_playlist`) REFERENCES `playlists` (`id`),
  ADD CONSTRAINT `user_favourite_playlists_ibfk_3` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `user_favourite_songs`
--
ALTER TABLE `user_favourite_songs`
  ADD CONSTRAINT `user_favourite_songs_ibfk_1` FOREIGN KEY (`id_song`) REFERENCES `songs` (`id`),
  ADD CONSTRAINT `user_favourite_songs_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
