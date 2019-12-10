import React, {Component} from 'react';
import FileDrop from 'react-file-drop';
import {apiService} from "./apiService";
import logo from './logo.svg';
import './App.css';


class App extends Component {

    constructor(props) {
        super(props);
        this.handleDrop = this.handleDrop.bind(this);
        this.state = {
            uploading: false,
            file: null,
            message: null
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

    render() {

        let files = [];
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
                </header>
            </div>
        );
    }
}

export default App;
