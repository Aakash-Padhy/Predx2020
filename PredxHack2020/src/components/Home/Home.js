import React from 'react';
import {Layout,Menu,Typography,Button,Row, Col} from 'antd';
import mainLogo from './mainLogo.jpeg';
import './Home.css';
const {Header, Content,Footer}=Layout;
const {Text}=Typography;
const Home = () => {
    return (
        <Layout className='layout' style={{minHeight:'100vh'}}>
            <Row className='covid'>
                <Col span={24}>
                <Text type='strong' style={{padding: '0 15px'}}>Let's Fight Covid-19 Together</Text>
                <Button danger>View Guidelines</Button>
                </Col>
            </Row>    
            <Header>
            <div className="logo" />
            <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
                <Menu.Item key="1">Home</Menu.Item>
                <Menu.Item key="2">Predict</Menu.Item>
                <Menu.Item key="3">About</Menu.Item>
            </Menu>
            </Header>
            <Layout className='main'>
                <Content>
                    <Row>
                        <Col span={10} className='white'>
                            <img src={mainLogo} alt="Logo" className="mainLogo"/>
                        </Col>
                        <Col className='mainContent' span={14}>
                            <Row className='rowDiv'>
                                <Col span={12}><Button type="primary" shape="circle" className='navBut'>
                                    PREDICT
                                </Button>
                                </Col>
                                <Col span={12}>
                                    <Button type="primary" shape="circle" className='navBut'>
                                    SYMPTONS
                                    </Button>
                                </Col>
                            </Row>
                            <Row className='rowDiv'>
                                <Col span={12}><Button type="primary" shape="circle" className='navBut'>
                                    LOGIN/REGISTER
                                </Button>
                            </Col>
                            <Col span={12}>
                                <Button type="primary" shape="circle" className='navBut'>
                                    MASTER
                                </Button>
                            </Col>
                            </Row>
                        </Col>
                    </Row> 
                </Content>
            </Layout>
            <Footer style={{ textAlign: 'center',padding:'12px 50px'}}>Predx ©2020 Created by Team Cinque</Footer>
        </Layout>
    );
}
 
export default Home;