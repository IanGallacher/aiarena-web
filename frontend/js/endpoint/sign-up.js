import React from "react";

import AlertLogic from "./../logic/alert.js";
import LoginLogic from "./../logic/login.js";

import { TextInput, PrimaryButton } from "./../component/form.jsx";

export default class SignUp extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      errors: [],
      username: "",
      email: "",
      password: "",
      password_confirmation: ""
    };
  }

  onChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  }

  onSubmit = (event) => {
    event.preventDefault();
    LoginLogic.signUp(this.state)
      .then(() => AlertLogic.addSuccess("Account created"))
      .catch(errors => this.setState({errors}));
  }

  render() {
    return (
      <form
        name="form-signup"
        className="flex-vertical form-container"
        onSubmit={this.onSubmit}
      >
        <h2 className="form-signup-heading">Register</h2>
        <TextInput name="username"
          type="text"
          error={this.state.errors.username && this.state.errors.username}
          placeholder="Username"
          onChange={this.onChange}
          autoFocus />

        <TextInput name="email"
          type="text"
          error={this.state.errors.email}
          placeholder="Email"
          onChange={this.onChange} />
        <br/>

        <TextInput name="password"
          type="password"
          error={this.state.errors.password}
          placeholder="Password"
          onChange={this.onChange} />

        <TextInput name="password_confirmation"
          type="password"
          error={this.state.errors.password_confirmation}
          placeholder="Confirm Password"
          onChange={this.onChange} />
        <br/>
        <PrimaryButton name="Submit" id="submit" label="Sign up"/>
      </form>
    );
  }
}
