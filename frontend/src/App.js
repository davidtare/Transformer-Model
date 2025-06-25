import React, { useState } from 'react';
import {
    Container,
    Typography,
    Box,
    Tabs,
    Tab,
    TextField,
    Button,
    Card,
    CardContent,
    Grid,
    Alert,
    CircularProgress,
    Snackbar,
    IconButton,
    Fade,
    ThemeProvider,
    CssBaseline
} from '@mui/material';
import { LightMode as LightModeIcon, DarkMode as DarkModeIcon } from '@mui/icons-material';
import { createAppTheme } from './theme';
import AnalysisResults from './components/AnalysisResults';
import TimeSeriesAnalysis from './components/TimeSeriesAnalysis';
import GoodsManagement from './components/GoodsManagement';
import { API_URL } from './vars';

function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ p: 3 }}>
                    {children}
                </Box>
            )}
        </div>
    );
}

function App() {
    const [darkMode, setDarkMode] = useState(false);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState('');
    const [value, setValue] = useState(0);

    const toggleDarkMode = () => {
        setDarkMode(!darkMode);
    };

    const showSnackbar = (message, severity = 'info') => {
        setSnackbar({ open: true, message, severity });
    };

    const analyzeText = async () => {
        if (!text.trim()) {
            setError('Please enter some text to analyze');
            return;
        }

        setLoading(true);
        setError('');
        setResults(null);

        try {
            const response = await fetch(`${API_URL}/api/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) {
                throw new Error('Analysis failed');
            }

            const data = await response.json();
            setResults(data);
            showSnackbar('Analysis completed successfully!', 'success');
        } catch (err) {
            setError('Failed to analyze text. Please try again.');
            showSnackbar('Analysis failed. Please try again.', 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const theme = createAppTheme(darkMode);

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Box sx={{
                minHeight: '100vh',
                bgcolor: 'background.default',
                transition: 'all 0.3s ease-in-out',
                paddingTop: '40px'
            }}>
                <Box sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}>
                    <Typography variant="h3" component="h1" gutterBottom sx={{
                        textAlign: 'center',
                        color: '#2c3e50',
                        fontWeight: 'bold',
                        mb: { xs: 2, sm: 4 },
                        mT: { xs: 2, sm: 4 },
                        textShadow: '2px 2px 4px rgba(0,0,0,0.1)'
                    }}>
                        Process Analysis Dashboard
                    </Typography>
                    <IconButton onClick={toggleDarkMode} color="primary"
                        sx={{ marginLeft: '130px' }}
                    >
                        {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
                    </IconButton>
                </Box>
                
                <Box sx={{
                    borderBottom: 1,
                    borderColor: 'divider',
                    mb: 3,
                    overflowX: 'auto',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}>
                    <Tabs
                        value={value}
                        onChange={handleChange}
                        variant="standard"
                        centered
                        sx={{
                            '& .MuiTab-root': {
                                fontSize: { xs: '0.875rem', sm: '1.1rem' },
                                fontWeight: 'medium',
                                textTransform: 'none',
                                minWidth: { xs: 'auto', sm: 200 },
                                color: '#546e7a',
                                '&.Mui-selected': {
                                    color: '#1976d2',
                                    fontWeight: 'bold',
                                },
                            },
                            '& .MuiTabs-indicator': {
                                backgroundColor: '#1976d2',
                                height: 3,
                                borderRadius: '3px 3px 0 0',
                            },
                            '& .MuiTabs-flexContainer': {
                                justifyContent: 'center',
                                gap: 2
                            }
                        }}
                    >
                        <Tab label="Text Analysis" />
                        <Tab label="Time Series Analysis" />
                        <Tab label="Goods Management" />
                    </Tabs>
                </Box>

                <TabPanel value={value} index={0}>
                    <Fade in={true} timeout={500}>
                        <Box sx={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            flexDirection: 'column'
                        }}>
                            {error && (
                                <Alert
                                    severity="error"
                                    sx={{
                                        mb: 2,
                                        borderRadius: 2,
                                        boxShadow: 1,
                                    }}
                                >
                                    {error}
                                </Alert>
                            )}

                            <Card elevation={3} sx={{
                                mb: 3,
                                width: '50%',
                                borderRadius: 3,
                                background: 'linear-gradient(145deg,rgb(118, 54, 54) 0%,rgb(112, 131, 151) 100%)',
                            }}>
                                <CardContent>
                                    <Grid container spacing={2}>
                                        <Grid item xs={12}>
                                            <TextField
                                                fullWidth
                                                multiline
                                                rows={4}
                                                variant="outlined"
                                                label="Enter text to analyze"
                                                value={text}
                                                onChange={(e) => setText(e.target.value)}
                                                error={!!error}
                                                helperText={error}
                                                sx={{
                                                    color: 'black',
                                                    '& .MuiOutlinedInput-root': {
                                                        borderRadius: 2,
                                                        backgroundColor: 'rgba(255,255,255,0.9)',
                                                        '&:hover': {
                                                            backgroundColor: 'rgba(255,255,255,1)',
                                                        },
                                                    },
                                                }}
                                            />
                                        </Grid>
                                        <Grid item xs={12}>
                                            <Button
                                                variant="contained"
                                                color="primary"
                                                onClick={analyzeText}
                                                disabled={loading}
                                                fullWidth
                                                sx={{
                                                    py: 1.5,
                                                    borderRadius: 2,
                                                    background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                                                    boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)',
                                                    '&:hover': {
                                                        background: 'linear-gradient(45deg, #1976D2 30%, #1CB5E0 90%)',
                                                    },
                                                }}
                                            >
                                                {loading ? <CircularProgress size={24} color="inherit" /> : 'Analyze Text'}
                                            </Button>
                                        </Grid>
                                    </Grid>
                                </CardContent>
                            </Card>

                            {results && (
                                <AnalysisResults results={results} />
                            )}
                        </Box>
                    </Fade>
                </TabPanel>

                <TabPanel value={value} index={1}>
                    <Fade in={true} timeout={500}>
                        <Card elevation={3} sx={{
                            borderRadius: 3,
                        }}>
                            <CardContent>
                                <TimeSeriesAnalysis />
                            </CardContent>
                        </Card>
                    </Fade>
                </TabPanel>

                <TabPanel value={value} index={2}>
                    <Fade in={true} timeout={500}>
                        <Card elevation={0} sx={{
                            borderRadius: 4,
                        }}>
                            <CardContent>
                                <GoodsManagement />
                            </CardContent>
                        </Card>
                    </Fade>
                </TabPanel>

                <Snackbar
                    open={snackbar.open}
                    autoHideDuration={6000}
                    onClose={() => setSnackbar({ ...snackbar, open: false })}
                    anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
                >
                    <Alert
                        onClose={() => setSnackbar({ ...snackbar, open: false })}
                        severity={snackbar.severity}
                        sx={{ width: '100%' }}
                    >
                        {snackbar.message}
                    </Alert>
                </Snackbar>
            </Box>
        </ThemeProvider>
    );
}

export default App;