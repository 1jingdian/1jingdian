# coding: utf-8
from datetime import datetime, date
from flask import g
from ._base import db
from ..utils.uploadsets import collection_covers


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    cover = db.Column(db.String(200), default="default.png")
    desc = db.Column(db.Text)

    kind_id = db.Column(db.Integer, db.ForeignKey('collection_kind.id'))
    kind = db.relationship('CollectionKind',
                           backref=db.backref('collections',
                                              lazy='dynamic',
                                              order_by='desc(Collection.created_at)'))

    @property
    def cover_url(self):
        return collection_covers.url(self.cover) if self.cover else ""

    @property
    def voted_pieces_by_user(self):
        from . import PieceVote, Piece

        if not g.user:
            return None
        return Piece.query \
            .filter(Piece.collections.any(CollectionPiece.collection_id == self.id)) \
            .filter(Piece.voters.any(PieceVote.user_id == g.user.id))

    def liked_by_user(self):
        return g.user and self.likers.filter(user_id=g.user.id).count() > 0

    def has_piece(self, piece_id):
        return self.pieces.filter(CollectionPiece.piece_id == piece_id).count() > 0

    def __repr__(self):
        return '<Collection %s>' % self.id


class CollectionKind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    name = db.Column(db.String(100))


class CollectionPiece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    collection = db.relationship('Collection',
                                 backref=db.backref('pieces',
                                                    lazy='dynamic',
                                                    order_by='desc(CollectionPiece.created_at)'))

    piece_id = db.Column(db.Integer, db.ForeignKey('piece.id'))
    piece = db.relationship('Piece',
                            backref=db.backref('collections',
                                               lazy='dynamic',
                                               order_by='asc(CollectionPiece.created_at)'))


class UserLikeCollection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('liked_collections',
                                              lazy='dynamic',
                                              order_by='desc(UserLikeCollection.created_at)'))

    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    collection = db.relationship('Collection',
                                 backref=db.backref('likers',
                                                    lazy='dynamic',
                                                    order_by='desc(UserLikeCollection.created_at)'))
