import React /*, {Component}*/ from "react";
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import AuthService from '../service/AuthService';
import PropTypes from "prop-types";

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" target="_blank" href="https://github.com/HyperTars/Online-Video-Platform/">
        Greloupis
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const styles = (theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
});

class Register extends  React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    this.state = {
      username: "",
      email: "",
      password: "",
      success: false,
      message: ""
    };
  }

  handleChange(event) {
    this.setState({
      username: event.state.username,
      email: event.state.email,
      password: event.state.password,
    })
  }

  handleSubmit(event) {
    event.preventDefault();
    this.setState({
      message: "",
      success: false
    });

    // this.form.validateAll();

    if (true) { // validate here
      AuthService.register(
        this.state.username, 
        this.state.email, 
        this.state.password
      ).then(
        response => {
          this.setState({
            message: response.message,
            success: true
          });
        },
        error => {
          const resMessage = 
            (error.response &&
              error.response.date &&
              error.response.data.message) ||
              error.message ||
              error.toString();
          this.setState({
            success: false,
            message: resMessage
          });

          console.log(this.state);
          alert("register failed");
        }
      );      
    } else {
      this.setState({
        loading: false,
      });
      alert("Invalid params");
    }
  }

  render() {
    const { classes } = this.props;

    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign up
          </Typography>
          <form className={classes.form} noValidate onSubmit={this.handleSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  variant="outlined"
                  autoComplete="username"
                  name="username"
                  required
                  fullWidth
                  id="username"
                  label="User Name"
                  autoFocus
                  value={this.state.username}
                  onChange={(event) =>
                    this.setState({
                      [event.target.name]: event.target.value
                    })
                  }
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  variant="outlined"
                  autoComplete="email"
                  name="email"
                  required
                  fullWidth
                  id="email"
                  label="User Email"
                  autoFocus
                  value={this.state.email}
                  onChange={(event) =>
                    this.setState({
                      [event.target.name]: event.target.value
                    })
                  }
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  variant="outlined"
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  value={this.state.password}
                  onChange={(event) =>
                    this.setState({
                      [event.target.name]: event.target.value
                    })
                  }
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={<Checkbox value="allowExtraEmails" color="primary" />}
                  label="I want to receive news and updates via email."
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
            >
              Sign Up
            </Button>
            <Grid container justify="flex-end">
              <Grid item>
                <Link href="/login" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </form>
        </div>
        <Box mt={5}>
          <Copyright />
        </Box>
      </Container>
    );
  }
}

Register.propTypes = {
  classes: PropTypes.object.isRequired
};

export default new withStyles(styles)(Register);