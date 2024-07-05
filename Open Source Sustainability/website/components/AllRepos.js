import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import axios from 'axios';
import { Router } from '@mui/icons-material';

function Row(props) {
    const { row } = props;
    const [open, setOpen] = useState(false);

    return (
        <React.Fragment>
            <TableRow sx={{ '& > *': { borderBottom: 'unset', textAlign: 'center' } }}>
                <TableCell>
                    <IconButton
                        aria-label="expand row"
                        size="small"
                        onClick={() => setOpen(!open)}
                    >
                        {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                    </IconButton>
                </TableCell>
                <TableCell component="th" scope="row">
                    <a href={'https://sage-milwaukee-domains-tapes.trycloudflare.com'} target='_blank'>
                        {row.name}
                    </a>
                </TableCell>
                <TableCell align="center">{row.issues.totalCount}</TableCell>
                <TableCell align="center">
                    <a href={row.url} target="_blank" rel="noopener noreferrer">
                        {row.url}
                    </a>
                </TableCell>
                <TableCell align="center">{row.isPrivate ? 'Yes' : 'No'}</TableCell>
            </TableRow>
        </React.Fragment>
    );
}

Row.propTypes = {
    row: PropTypes.shape({
        issues: PropTypes.shape({
            totalCount: PropTypes.number.isRequired,
        }).isRequired,
        name: PropTypes.string.isRequired,
        url: PropTypes.string.isRequired,
        isPrivate: PropTypes.bool.isRequired,
    }).isRequired,
};

export default function CollapsibleTable() {
    const [data, setData] = useState([]);

    useEffect(() => {
        let username = sessionStorage.getItem("username");
        console.log(username);
        axios
            .get("/api/getAllRepos", { params: { username: username } })
            .then((res) => {
                const json = JSON.parse(JSON.stringify(res.data));
                let arr = json.viewer.repositories.nodes;
                arr = Array.from(arr);
                console.log(arr);
                console.log(typeof arr);
                setData(arr);
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);

    return (
        <TableContainer component={Paper}>
            <Table aria-label="collapsible table">
                <TableHead>
                    <TableRow>
                        <TableCell />
                        <TableCell>Repository Name</TableCell>
                        <TableCell>Issues</TableCell>
                        <TableCell>URL</TableCell>
                        <TableCell>Private</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {data.map((row) => (
                        <Row key={row.name} row={row} />
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
