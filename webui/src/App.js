import React, {Component} from 'react';
import FileDrop from 'react-file-drop';
import 'bootstrap/dist/css/bootstrap.css';
import {
    Button, Modal, Col, Container, Dropdown, DropdownButton,
    FormControl, InputGroup, Row, Table, Form
} from "react-bootstrap";

import {apiService} from "./apiService";
import './App.css';


class App extends Component {

    constructor(props) {
        super(props);
        this.handleDrop = this.handleDrop.bind(this);
        this.state = {
            uploading: false,
            file: null,
            message: null,
            devpacks: [],
        }
    }

    handleDrop(files, event) {
        if (files.length == 0) return;
        this.setState({
            file: files[0],
            uploading: true
        }, () => {
            const data = new FormData();
            data.append('file', files[0]);
            apiService.post("/api/package", data, {
                asForm: true
            }).then(r => r.json())
                .then(r => {
                    let message = `Package ${r.pkginfo.package}==${r.pkginfo.version} was uploaded`;
                    this.setState({
                        message: message,
                        uploading: false
                    }, ()=>{
                        setTimeout(()=>{
                            this.setState({message: null, uploading: false})
                        }, 1000 * 10);
                    })
                })
                .catch(e => {
                    this.setState({
                        message: "Error: " + e,
                        uploading: false
                    }, ()=>{
                        setTimeout(()=>{
                            this.setState({message: null, uploading: false})
                        }, 1000 * 10);
                    })
                    console.log("Error ocurred!", e);
                })
        });

    }

    componentDidMount() {
        apiService.get("/api/devices_packages")
            .then(r=>r.json())
            .then(r=>{
                this.setState({
                    devpacks: r
                })
            })
            .catch(e=>{
                console.log(e);
                alert("Error occurred while fetching devices and packages: " + e)
            })
    }

    render() {

        let files = [];
        let devpacks = this.state.devpacks || []
        const styles = {border: '1px dashed black', width: '80%', height: '80%', color: 'white'};
        return (
            <div className="App">
                <header className="App-header">
                    <div id="react-file-drop-demo" style={styles}>
                        <FileDrop onDrop={this.handleDrop} style={{
                            width: '100%',
                            height: '100%',
                            display: 'inline-block'
                        }}>
                            {(() => {
                                if (this.state.uploading) {
                                    return (<p>
                                        Your package is uploading
                                    </p>)
                                } else if(this.state.message){
                                    return (<p>
                                        {this.state.message}
                                    </p>)
                                }else {
                                    return (<p>
                                        Drop your signed APK.
                                    </p>)
                                }

                            })()}
                        </FileDrop>
                    </div>
                    <Container>
                        <h2>Devices and packages</h2>
                        <Table striped bordered hover>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Serial</th>
                                <th>Ip</th>
                                <th>Mac</th>
                                <th>Package</th>
                                <th>Version</th>
                            </tr>
                        </thead>
                        <tbody>
                        {devpacks.map((d, i)=>{
                            let dev = d.device;
                            let packages = d.packages;
                            return packages.map((p, ipx)=>{
                                return (<tr key={i + ipx}>
                                    <td>{i + ipx}</td>
                                    <td>{dev.serial}</td>
                                    <td>{dev.ip}</td>
                                    <td>{dev.mac}</td>
                                    <td>{p.name}</td>
                                    <td>{p.version}</td>
                                </tr> )
                            });
                        })}
                        </tbody>
                    </Table>
                    </Container>

                </header>
            </div>
        );
    }
}

export default App;
