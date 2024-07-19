// PlaylistContext.js

import React, { createContext, useState } from 'react';
import dummyData from '../app/Mock/Dummy';

export const PlaylistContext = createContext();

export const PlaylistProvider = ({ children }) => {
  const [playlists, setPlaylists] = useState(dummyData.Playlists);

  const addPlaylist = (newPlaylist) => {
    setPlaylists([...playlists, newPlaylist]);
  };

  const removePlaylist = (playlistId) => {
    setPlaylists(playlists.filter((p) => p.id !== playlistId));
  };

  return (
    <PlaylistContext.Provider value={{ playlists, addPlaylist, removePlaylist }}>
      {children}
    </PlaylistContext.Provider>
  );
};
