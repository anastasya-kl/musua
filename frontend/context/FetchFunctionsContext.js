import React, { createContext } from 'react';

export const FetchFunctionsContext = createContext({
  fetchPlaylistData: () => {},
  fetchReccData: () => {},
});