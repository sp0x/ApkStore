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
            predicting: false,
            file: null
        }
    }

    handleDrop(files, event) {
        if (files.length == 0) return;
        this.setState({
            file: files[0],
            predicting: true
        }, () => {
            const data = new FormData();
            data.append('file', files[0]);
            apiService.post("/api/forecast_file", data, {
                asForm: true
            }).then(r => r.blob())
                .then(b => {
                    const url = window.URL.createObjectURL(new Blob([b]))
                    const link = document.createElement("a");
                    link.href = url;
                    link.setAttribute('download', 'prediction.csv');
                    document.body.appendChild(link)
                    link.click();
                    link.parentNode.removeChild(link)
                    this.setState({
                        predicting: false
                    })
                })
                .catch(e => {
                    console.log("Error ocurred!");
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
                                if (this.state.predicting) {
                                    return (<p>
                                        Please wait for your prediction file...
                                    </p>)
                                } else {
                                    return (<p>
                                        Drop your CSV here to get predictions
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
