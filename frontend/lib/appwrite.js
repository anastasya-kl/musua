import { Account, Avatars, Client, Databases, ID, Query } from "react-native-appwrite";
import axios from 'axios';
import React, {useState, useEffect } from "react";

export const config = {
    endpoint: "https://cloud.appwrite.io/v1",
    platform: 'com.jsm.musua',
    projectId: '6637aac70030eb6604ad',
    databaseId: '6637ae2e003b952349da',
    userCollectionId: '6637ae960017b50d00ac',
    songCollectionId: '6637aef6002d8bef6fe6',
    storageId: '6637c2ff001c654743f4'
};

const {
    endpoint,
    platform,
    projectId,
    databaseId,
    userCollectionId,
    songCollectionId,
    storageId,
} = config;

const client = new Client();

client
    .setEndpoint(endpoint) 
    .setProject(projectId) 
    .setPlatform(platform); 

const account = new Account(client);
const avatars = new Avatars(client);
const databases = new Databases(client);
  

// Register user
export async function createUser(email, password, username) {

    try {

        const newAccount = await account.create(
            ID.unique(),
            email, 
            password, 
            username
        );

        if(!newAccount) throw Error;

        console.log("accountId:", newAccount.$id);
        console.log(newAccount.$id);
        
        const response = await axios.post('http://192.168.1.106:8080/api/sign_up_user/', {
            user_id: newAccount.$id,
            nickname: username,
            password: password,
            email: email
            });
        console.log(response.data);

        const avatarUrl = avatars.getInitials(username);
        await signIn(email, password);
        const newUser = await databases.createDocument(
            config.databaseId,
            config.userCollectionId,
            ID.unique(),
            {
                accountId: newAccount.$id,
                email, 
                username,
                avatar: avatarUrl
            }
        );
        
        return newUser;
    } catch (error) {
        console.log(error);
        throw new Error(error);
    }
}

//Sign In
export async function signIn(email, password) {
    try {
        const session = await account.createEmailPasswordSession(email, password);
        return session;
    } catch (error) {
        throw new Error(error);
    }
}

// Get Account
export async function getAccount() {
    try {
      const currentAccount = await account.get();
      
      return currentAccount;
    } catch (error) {
      throw new Error(error);
    }
  }

export async function getUserID() {
    try {
      const currentAccount = await account.get();
      return currentAccount.$id;
    } catch (error) {
      throw new Error(error);
    }
  }

//Get Current User
export async function getCurrentUser() {
    try {
        const currentAccount = await getAccount();
        if(!currentAccount) throw Error;
        const currentUser = await databases.listDocuments(
            config.databaseId,
            config.userCollectionId,
            [Query.equal('accountId', currentAccount.$id)]
        )

        if(!currentUser) throw Error;

        return currentUser.documents[0];
    } catch (error) {
        console.log(error);
        return null;
    }
}

// Get All Posts
export async function getAllPosts() {
    try {
        const posts = await databases.listDocuments(
            databaseId,
            songCollectionId
        )

        return posts.documents;
    } catch (error) {
        throw new Error(error);
    }
}

// Get All Posts
export async function getLatestPosts() {
    try {
        const posts = await databases.listDocuments(
            databaseId,
            songCollectionId,
            [Query.orderDesc('$createdAt', Query.limit(7))]
        )

        return posts.documents;
    } catch (error) {
        throw new Error(error);
    }
}

export const searchPosts = async (query) => {
    try {
        const posts = await databases.listDocuments(
            databaseId,
            songCollectionId,
            [Query.search('title', query)]
        )

        return posts.documents;
    } catch (error) {
        throw new Error(error);
    }
}

export const signOut = async () => {
    try {
        const session = await account.deleteSession ('current');

        return session;
    } catch (error) {
        throw new Error(error)
    }
}