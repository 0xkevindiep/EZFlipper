import React from "react";
import ReactDOM from "react-dom";
import { act } from "react-dom/test-utils";
import Home from "../src/pages/Home";

var assert = require("assert");
var jsdom = require("mocha-jsdom");

global.document = jsdom({
    url: "http://localhost:3000/"
});

let rootContainer;

beforeEach(() => {
    rootContainer = document.createElement("div");
    document.body.appendChild(rootContainer);
});

describe("Home", () => {
    it("Describes the Home page", () => {
        act(() => {
            ReactDOM.render(<Home />, rootContainer);
            var divCount = rootContainer.getElementsByTagName("div").length;
            assert.strictEqual(divCount, 2);
        });
    });
  });

afterEach(() => {
    document.body.removeChild(rootContainer);
    rootContainer = null;
});