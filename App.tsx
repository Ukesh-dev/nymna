import { Image, ImageBackground, StatusBar, StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React, { useEffect, useState } from 'react'
import { OneSignal } from 'react-native-onesignal'
import Modal from "react-native-modal";

export default function App() {

    const [visible, setVisible] = useState<boolean>(false);
    const [notiData, setNotiData] = useState<any>(null)

    const getStatuscolor = (status : string) => {
        try {
            if(status == "minor"){
                return "rgba(21, 128, 61, 1)"
            }else if(status == "mediocre"){
                return "rgba(180, 83, 9, 1)"
            }else if(status == "severe"){
                return "rgba(185, 28, 28, 1)"
            }
        } catch (error) {
            return "#fff"
        }
    }

    const getStatusbgcolor = (status : string) => {
        try {
            if(status == "minor"){
                return "rgba(220, 252, 231, 1)"
            }else if(status == "mediocre"){
                return "rgba(254, 243, 199, 1)"
            }else if(status == "severe"){
                return "rgba(254, 226, 226, 1)"
            }
        } catch (error) {
            return "#000"
        }
    }

    useEffect(() => {
        OneSignal.initialize("b45d498d-4c33-417e-b842-d6009d3873cd")
        OneSignal.Notifications.requestPermission(true);
        OneSignal.Notifications.addEventListener('click', (event) => {
            const additionalData = event.notification.additionalData;
            if (additionalData){
                setVisible(true)
                setNotiData(additionalData)
            }
        });
    }, [])
    

    return (
        <View style={{
            flex : 1
        }}>
            <StatusBar backgroundColor="rgba(0, 0, 0, 1)" />
            <Modal
                isVisible={visible}
                onBackdropPress={() => setVisible(false)}
            >
                <View style={{ 
                    backgroundColor: 'rgba(17, 24, 39, 0.75)',
                    justifyContent: 'center',
                    alignItems: 'center',
                    borderRadius: 10,
                    padding: 35
                }}>
                    <View style={{
                        display:"flex",
                        flexDirection:"row",
                        alignItems:"center",
                        justifyContent:"center",
                        backgroundColor:"rgba(254, 226, 226, 1)",
                        padding:10,
                        borderRadius:100
                    }}>
                        <Image
                            source={require("./src/components/file.png")}
                            style={{
                                width: 50,
                                height: 50
                            }}
                        />
                    </View>
                    
                    <Text style={{
                        fontSize:27,
                        fontWeight:"bold",
                        color:"#fff",
                        marginTop:10
                    }}>Incident Alert</Text>

                    <Text style={{
                        fontSize:18,
                        color:"#fff",
                        marginTop:0
                    }}>There has been an incident.</Text>

                    {
                        notiData &&
                        <View style={{
                            backgroundColor:getStatusbgcolor(notiData.status),
                            borderRadius:5,
                            display:"flex",
                            alignItems:"center",
                            justifyContent:"center",
                            paddingVertical:5,
                            marginTop:20,
                            paddingHorizontal:10
                        }}>
                            <Text style={{
                                fontSize:17,
                                color:getStatuscolor(notiData.status),
                                textTransform:"capitalize"
                            }}>Status: <Text style={{
                                fontWeight:"bold"
                            }}>{notiData.status}</Text></Text>
                        </View>
                    }

                    <TouchableOpacity style={{
                        backgroundColor:"rgba(220, 38, 38, 1)",
                        borderRadius:5,
                        display:"flex",
                        alignItems:"center",
                        justifyContent:"center",
                        paddingVertical:10,
                        marginTop:30,
                        paddingHorizontal:10
                    }}>
                        <Text style={{
                            color:"#fff",
                            fontWeight:"bold"
                        }}>Check Details</Text>
                    </TouchableOpacity>
                </View>
            </Modal>

            <ImageBackground
                source={require("./src/components/back.jpeg")}
                style={{
                    flex : 1,
                    display:"flex",
                    alignItems:"center",
                    justifyContent:"center"
                }}
                blurRadius={10}
                resizeMode="cover"
            >
                <Image
                    source={require("./src/components/logo.png")}
                    style={{
                        width:150,
                        height:150,
                        marginBottom:20
                    }}
                />
                <Text style={{
                    color:"#fff",
                    fontWeight:"bold",
                    fontSize:25
                }}>ANAMOLY DETECTION</Text>
                <Text style={{
                    color:"#999",
                    fontWeight:"500",
                    fontSize:17
                }}>NYMNA</Text>
            </ImageBackground>
        </View>
    )
}

const styles = StyleSheet.create({})