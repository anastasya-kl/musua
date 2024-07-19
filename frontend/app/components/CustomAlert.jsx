import React, { useState } from 'react';
import { Modal, View, Text, TouchableOpacity } from 'react-native';

const CustomAlert = ({ visible, onCancel, onConfirm }) => {
  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onCancel}
    >
      <View style={{ marginLeft: 20, marginRight: 20, flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
        <View className="bg-[#f5f5f5] px-4 py-10 rounded-[16px] w-[340px]">
          <View className="flex-row justify-center">
          <TouchableOpacity onPress={onConfirm} className="rounded-[4px] bg-[#FF5B5B] w-[140px] py-2 items-center mr-[8px]">
              <Text className="text-black font-regular text-[16px]">Видалити</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={onCancel} className="rounded-[4px] w-[140px] py-2 items-center bg-gray-100">
              <Text className="text-black font-regular text-[16px]">Скасувати</Text>
            </TouchableOpacity>
            
          </View>
        </View>
      </View>
    </Modal>
  );
};

export default CustomAlert;
